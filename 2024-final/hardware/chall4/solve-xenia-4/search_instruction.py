import struct

import capstone
cs = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)

KEY_BITS = {
    1: '#',
    2: '0',
    3: '*',
    4: '7',
    5: '8',
    6: '9',
    9: '6',
    10: '5',
    11: '4',
    12: '3',
    13: '2',
    14: '1',
}


for i in range(0x10000):
    insts = list(cs.disasm(struct.pack("I", i), 0))
    if len(insts) == 0:
        continue

    inst = insts[0]

    if inst.mnemonic in ('bx', 'blx') and inst.op_str == "r0":
        print(hex(i), f"{i:016b}", inst)
        for b in range(16):
            if (i >> b)&1 == 0:
                print(f"bit {b} ({KEY_BITS.get(b)})")
