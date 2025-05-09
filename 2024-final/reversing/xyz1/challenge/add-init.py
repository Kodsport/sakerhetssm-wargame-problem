#!/usr/bin/env python3

import sys
import struct
import lief
from keystone import *

target_path = sys.argv[1]
base_path = sys.argv[2]
hook_path = sys.argv[3]

print(
    f'Patching "{base_path}" with hook "{hook_path}" and saving to "{target_path}"'
)

base_elf = lief.parse(base_path)
hook_elf = lief.parse(hook_path)


def copy_hook_data(base_elf, hook_elf):
    hook_symbol = hook_elf.get_symbol("hook")

    # Copy .text segment to target
    code_segment = hook_elf.segment_from_virtual_address(hook_symbol.value)
    segment_added = base_elf.add(code_segment)

    # Optionally, copy .rodata segment to target
    rodata_section = hook_elf.get_section('.rodata')
    if rodata_section:
        rodata_segment = hook_elf.segment_from_virtual_address(
            rodata_section.virtual_address)
        segments_delta = rodata_segment.virtual_address - code_segment.virtual_address
        segment_added2 = base_elf.add(rodata_segment)
        new_rodata_address = segment_added.virtual_address + segments_delta
        print(f'.rodata address: {new_rodata_address:#x}')
        segment_added2.virtual_address = new_rodata_address

    got_section = hook_elf.get_section('.got')
    if got_section:
        print(got_section)
        got_segment = hook_elf.segment_from_virtual_address(
            got_section.virtual_address)
        print(
            f'old .got: {got_segment.virtual_address:#x}, old .text {code_segment.virtual_address:#x}'
        )
        segments_delta = got_segment.virtual_address - code_segment.virtual_address
        print(f'GOT delta: {segments_delta:#x}')
        segment_added3 = base_elf.add(got_segment)
        new_got_address = (segment_added.virtual_address +
                           segments_delta) & ~0xFFF
        segment_added3.virtual_size += 0x1000
        print(segment_added3, segment_added3.virtual_size)
        print(f'GOT address: {new_got_address:#x}')
        segment_added3.virtual_address = new_got_address

    hook_offset = hook_symbol.value - code_segment.virtual_address
    return segment_added, hook_offset


def patch_init(base_elf, hook_address):
    # Get current init info
    init_entry = base_elf[lief.ELF.DynamicEntry.TAG.INIT]
    init_section = base_elf.get_section('.init')
    init_segment = base_elf.segment_from_virtual_address(
        init_section.virtual_address)

    # Create new .init segment
    new_init_segment = lief.ELF.Segment()
    new_init_segment.flags = init_segment.flags
    new_init_segment.alignment = init_segment.alignment
    new_init_segment.type = init_segment.type
    new_init_segment.content = list(b'\0' * 100)
    new_init_segment.file_offset = 0
    new_init_segment_added = base_elf.add(new_init_segment)

    # Update .init section
    init_entry.value = new_init_segment_added.virtual_address
    original_init_address = init_section.virtual_address
    init_section.virtual_address = new_init_segment_added.virtual_address
    init_section.size = len(new_init_segment_added.content)

    # Assemble .init code
    # Note: stack is 16-byte aligned, "sub rsp, 8" to allow called functions to assume 16-byte alignment
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    new_init_asm = """
    sub rsp, 8
    call {init_addr:#x}
    call {hook_addr:#x}
    add rsp, 8
    ret
    """.format(**{
        'init_addr': original_init_address,
        'hook_addr': hook_address
    }).strip()
    new_init, _ = ks.asm(new_init_asm, addr=init_section.virtual_address)
    new_init_segment_added.content = list(new_init)


def fix_import_stubs(base_elf, hook_elf, new_hook_segment):
    hook_symbol = hook_elf.get_symbol("hook")
    # Copy segments to target
    hook_segment = hook_elf.segment_from_virtual_address(hook_symbol.value)

    fixed = set()
    for stub_symbol in hook_elf.symbols:
        if not stub_symbol.name.startswith('stub_'):
            continue
        if stub_symbol.name in fixed:  # Why do they appear twice?
            continue
        fixed.add(stub_symbol.name)

        # Calculate new VA for stub
        stub_offset = stub_symbol.value - hook_segment.virtual_address
        new_stub_address = new_hook_segment.virtual_address + stub_offset

        # Calculate jmp offset
        stub_target_name = stub_symbol.name.lstrip('stub_')
        stub_target_reloc = base_elf.get_relocation(stub_target_name)
        if not stub_target_reloc:
            print(f'ERROR: could not find {stub_target_name} in target')

        stub_code = bytes(
            base_elf.get_content_from_virtual_address(new_stub_address, 64))
        jmp_placeholder_offset = stub_code.index(struct.pack('<i', 0x77777777))
        jmp_ins_offset = jmp_placeholder_offset - 2
        jmp_va = new_stub_address + jmp_ins_offset
        after_jmp_va = jmp_va + 6
        rel_jmp = stub_target_reloc.address - after_jmp_va

        # Patch stub
        print(
            f'Rel jmp: {jmp_va:#x} -> {stub_target_reloc.address:#x} ({rel_jmp:#x})'
        )
        base_elf.patch_address(jmp_va + 2, list(struct.pack('<i', rel_jmp)))


hook_segment, hook_offset = copy_hook_data(base_elf, hook_elf)
hook_virtual_address = hook_segment.virtual_address + hook_offset
print(f'Hook address: {hook_virtual_address:#x}')
patch_init(base_elf, hook_virtual_address)
fix_import_stubs(base_elf, hook_elf, hook_segment)

base_elf.write(target_path)
