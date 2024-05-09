#!/usr/bin/env python3
from pwn import *

r = remote("localhost", 50000)

for _ in range(100):
    r.readuntil(b"collision: ")
    pt = bytes.fromhex(r.readline().decode())
    pt += b" "
    r.sendline(pt.hex().encode())

r.interactive()
