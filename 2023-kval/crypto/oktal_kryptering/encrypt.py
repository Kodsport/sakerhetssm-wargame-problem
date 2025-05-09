#!/usr/bin/env python3
import math, itertools, random

key = "01234567"
bits = int(math.log2(len(key)))

def new_key(k):
    k = list(k)
    random.shuffle(k)
    return ''.join(k)

def byte2bits(b):
    return bin(b)[2:].rjust(8, "0")

def pad(m):
    return m.ljust(len(m) + ((-len(m)) % bits), "0")

def encrypt(m):
    k = new_key(key)
    mbits = pad(''.join(map(byte2bits, m)))
    c = ""
    for i in range(0, len(mbits), bits):
        c += k[int(mbits[i:i + bits], 2)]
    # Anstalten®️-TODO: save key somewhere
    return c

with open("flag.txt", "rb") as f:
    flag = f.read()

with open("out.txt", "w") as f:
    f.write(encrypt(flag))
