#!/usr/bin/env python3
from Crypto.Util.number import *
from flag import FLAG

def gen_key():
    e = 0x10001
    p = getPrime(1024)
    q = getPrime(1024)
    d = pow(e, -1, (p - 1)*(q - 1))
    return d, (e, p*q)

def sign(m, priv_key, public_key):
    h = bytes_to_long(m.encode())
    sig = pow(h, priv_key, public_key[1])
    return sig

def verify(m, sig, public_key):
    h = pow(sig, public_key[0], public_key[1])
    return bytes_to_long(m.encode()) % public_key[1] == h

priv_key, public_key = gen_key()

m = input(f'Welcome to the BlackSmith! Here is our business card: {public_key}. What would you like to craft: ')
if not m.isalnum() or len(m) < 8:
    print("Don't try to scam us!!!")
    exit()

m1 = input('I can give you two samples of our craftmanship. What would you first like a sample of: ')
if not m1.isalnum():
    print("Don't try to scam us!!!")
    exit()

m2 = input('What else: ')
if not m2.isalnum():
    print("Don't try to scam us!!!")
    exit()

if m1 == m or m2 == m or m1 == m2:
    exit()

sig1 = sign(m1, priv_key, public_key)
sig2 = sign(m2, priv_key, public_key)

sig = int(input(f'Here are our samples: ({sig1}, {sig2}). Give us the necessary materials, and we shall deliver what you asked for: '), 16)

if verify(m, sig, public_key):
    print(FLAG)
else:
    print("Don't try to scam us!!!")
