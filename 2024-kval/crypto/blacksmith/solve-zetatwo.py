#!/usr/bin/env python3

import ast
from pwn import *
from z3 import *

HOST = 'localhost'
PORT = 50000

m1 = BitVec('a', 32)
m2 = BitVec('b', 32)
m0 = ZeroExt(32, m1) * ZeroExt(32, m2)

s = Solver()
def z3_isalnum(b):
    return Or(
        And(b >= 0x30, b < 0x3A),
        And(b >= 0x41, b < 0x5B),
        And(b >= 0x61, b < 0x7B),
    )

for i in range(4):
    b1 = Extract(8*i+7, 8*i, m1)
    s.add(z3_isalnum(b1))
for i in range(4):
    b2 = Extract(8*i+7, 8*i, m2)
    s.add(z3_isalnum(b2))
for i in range(8):
    b0 = Extract(8*i+7, 8*i, m0)
    s.add(z3_isalnum(b0))

if s.check() == sat:
    m = s.model()
    v1 = m[m1].as_long()
    v2 = m[m2].as_long()
    log.info('v1 = %d, v2 = %d', v1, v2)
else:
    log.critical('Failed to find values')
    sys.exit()

io = remote(HOST, PORT, level='info')
io.recvuntil(b'Welcome to the BlackSmith! Here is our business card: ')
card = io.recvuntil(b'.').decode()[:-1]
card = ast.literal_eval(card)
e, N = card

io.recvuntil(b'What would you like to craft: ')

v0 = v1*v2

io.sendline(v0.to_bytes(8, 'big'))

io.recvuntil(b'What would you first like a sample of: ')
io.sendline(v1.to_bytes(4, 'big'))
io.recvuntil(b'What else: ')
io.sendline(v2.to_bytes(4, 'big'))

io.recvuntil(b'Here are our samples: ')
samples = io.recvuntil(b'.').decode()[:-1]
samples = ast.literal_eval(samples)
s1, s2 = samples

s0 = (s1*s2) % N

io.recvuntil(b'Give us the necessary materials, and we shall deliver what you asked for: ')
io.sendline(f'{s0:#x}'.encode())
flag = io.recvline().decode().strip()
log.info('Flag: %s', flag)
