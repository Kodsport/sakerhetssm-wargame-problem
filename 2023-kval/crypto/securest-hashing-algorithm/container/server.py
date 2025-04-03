#!/usr/bin/env python3
from secrets import FLAG, ADMIN_PASSWORD
import hashlib

CHUNK_SIZE = 16

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def sha256(data):
    h = hashlib.sha256()
    h.update(data)
    return h.digest()

def hash_block(blk):
    h1 = sha256(bytes(blk, "ascii"))
    h2 = sha256(h1)
    return h2

def split_blocks(inp):
    return (inp[i:i+CHUNK_SIZE] for i in range(0, len(inp), CHUNK_SIZE))

def securest_hash(inp):
    blks = split_blocks(inp)
    hashes = [hash_block(blk) for blk in blks]
    result = hashes[0]
    for h in hashes[1:]:
        result = xor(result, h)
    return result

ADMIN_HASH = securest_hash(ADMIN_PASSWORD)

#TODO: Remove debug output?
print(ADMIN_HASH.hex())

while True:
    data = input("Enter password: ")
    hsh = securest_hash(data)
    if hsh == ADMIN_HASH:
        print("Correct! The flag is: " + FLAG)
        break
    else:
        print("Incorrect!")
