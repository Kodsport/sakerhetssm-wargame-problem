#!/usr/bin/env python3
from pwn import *
from Crypto.Cipher import AES
import base64

def xor(a, b):
    return bytes([x ^ y for (x, y) in zip(a, b)])

def register(username):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"> ", username)
    r.readuntil(b" profile: ")
    return r.readline()

def login(profile):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"> ", profile)

r = remote("localhost", 50000)

# admin=false&username=AAAAAAAAAAABBBBBBBBBBBBBBBB
# admin=false&username=AAAAAAAAAAA&admin=true&a=bb
username = b"A"*11 + b"B"*16
ct = base64.b64decode(register(username))

ct = ct[:-16] + xor(ct[-16:], xor(b"BBBBBBBBBBBBBBBB", b"&admin=true&a=bb"))

login(base64.b64encode(ct))

r.interactive()
