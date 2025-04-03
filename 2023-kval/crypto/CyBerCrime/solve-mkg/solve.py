#!/usr/bin/env python3
from pwn import *
from Crypto.Cipher import AES

def pad(msg, length=16):
    n = (-len(msg)) % length
    return msg + bytes([0]*n)

def sendmsg(msg):
    r.sendlineafter(b"ata to be decrypted:\n", msg.hex().encode())
    r.readuntil(b"Your decrypted data is ")
    ct = bytes.fromhex(r.readline()[:-1].decode())
    r.readuntil(b"Your data is ")
    score = float(r.readuntil(b"%")[:-1])
    r.readline()
    return ct, score/100.0*len(ct)*8.0

def decrypt(msg, key):
    return AES.new(key, AES.MODE_CBC, iv=key).decrypt(msg)

def encrypt(msg, key):
    return AES.new(key, AES.MODE_CBC, iv=key).encrypt(msg)

def score_me(flag, byte):
    ct = pad(flag + bytes([byte]))
    _, score1 = sendmsg(ct)
    _, score2 = sendmsg(ct + zero_ct)
    return score2 - score1

r = remote("127.0.0.1", 50000)
#r = process("./local-service.py", stderr=2)

# Get the iv / key
ct = b"A"*32
pt, _ = sendmsg(ct)
key = xor(ct[:16], pt[16:], pt[:16])
assert decrypt(ct, key) == pt

zero_ct = AES.new(key, AES.MODE_ECB).encrypt(b"\x00"*16)
assert AES.new(key, AES.MODE_ECB).decrypt(zero_ct) == b"\x00"*16

# Random assertion
pt, score = sendmsg(zero_ct*2)
assert pt[:16] == key and pt[16:] == zero_ct

flag = b""
while True:
    byte = 0
    for i in range(8):
        s1 = score_me(flag, byte | (1 << i))
        s2 = score_me(flag, byte)
        if s1 > s2:
            byte |= (1 << i)
        print("i:", i, s1, s2, int(s1 > s2), flag + bytes([byte]))
    flag += bytes([byte])
    try:
        print(flag.decode())
    except:
        print(flag)
print(flag.decode())

r.interactive()
