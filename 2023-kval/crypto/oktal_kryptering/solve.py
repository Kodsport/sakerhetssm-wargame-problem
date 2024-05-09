#!/usr/bin/env python3
import itertools, math

def int2bits(b, bits):
    return bin(b)[2:].rjust(bits, "0")

def decrypt(c, k):
    bits = int(math.log2(len(k)))
    mbits = "".join([int2bits(k.index(x), bits) for x in c])
    mbits = mbits[:len(mbits) - (len(mbits) % 8)]
    return bytes([int(mbits[i:i+8], 2) for i in range(0, len(mbits), 8)])

with open("out.txt") as f:
    c = f.read()

for k in itertools.permutations("01234567"):
    m = decrypt(c, k)
    if m.startswith(b"SSM"):
        print(''.join(k), m)
print("done")
