#!/usr/bin/env python3
import math, itertools, random

with open("out.txt", "r") as f:
    flag_encrypted = f.read().strip()

key = "01234567"
bits = int(math.log2(len(key)))

def byte2bits(b, nbits=8):
    return bin(b)[2:].rjust(nbits, "0")

def pad(m):
    return m.ljust(len(m) + ((-(len(m) % bits))) % bits, "0")

def encrypt_with_key(m, k):
    mbits = pad(''.join(map(byte2bits, m)))
    c = ""
    for i in range(0, len(mbits), bits):
        c += k[int(mbits[i:i + bits], 2)]
    # Anstalten®️-TODO: save key somewhere
    return c

def decrypt(e, k):
    mbits = ""
    for ch in e:
        n = k.index(int(ch))
        mbits += byte2bits(n, nbits=3)

    m = bytes()
    for i in range(0, len(mbits), 8):
        m = m + bytes([int(mbits[i:i+8], 2)])

    return m

known = b"SSM{"

known_encoded = encrypt_with_key(known, key)
print(known_encoded)
print(flag_encrypted)

# Fill in all known parts
decrypted_key = [None for _ in range(len(key))]
for i, (encoded, encrypted) in enumerate(zip(flag_encrypted, known_encoded)):
    encoded, encrypted = int(encoded), int(encrypted)
    if decrypted_key[encrypted] is not None and decrypted_key[encrypted] != encoded:
        print("mismatch at", i)
        exit(1)
    decrypted_key[encrypted] = encoded

# we have two unknowns: 0 and 7
assert decrypted_key[0] is None
assert decrypted_key[7] is None
assert all(x is not None for x in decrypted_key[1:7])

decrypted_key[0] = 7
decrypted_key[7] = 6
print("Attempt 1:", decrypt(flag_encrypted, decrypted_key))
decrypted_key[0] = 6
decrypted_key[7] = 7
print("Attempt 2:", decrypt(flag_encrypted, decrypted_key))
