#!/usr/bin/env python3

from ctypes import CDLL, c_uint64
from pwn import *

HOST = 'localhost'
PORT = 1337

NULL = 0

libc = CDLL('libc.so.6')
password: c_uint64 = c_uint64(1)

p = remote(HOST, PORT)
libc.srand(libc.time(NULL))
print(str(p.recvline(), 'utf-8'))

for i in range(5):
    password = c_uint64(password.value * libc.rand())
p.sendline(str(password.value))
print(str(p.recvline(), 'utf-8'))
