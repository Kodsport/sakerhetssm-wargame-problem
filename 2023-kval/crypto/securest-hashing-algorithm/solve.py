#!/usr/bin/env python3
import numpy as np
import galois
import hashlib
import random
import string

target = bytes.fromhex("6f520d05881ee30555aea7d0878ef923aa4e29e2235303cb032174e95f8bbe3f")

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

def binpad(x):
    o = bin(x)[2:]
    return "0" * (8 - len(o)) + o

def byte_2_bits(b):
    bs = [int(x) for x in binpad(b)]
    return bs

def bytes_2_bits(b):
    bits = []
    for byte in b:
        bits += byte_2_bits(byte)
    return bits

def random_blk():
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=16))

def gen_mat(s):
    mat = initial
    for a in s[::-1]:
        mat = np.insert(mat, 0, bytes_2_bits(hash_block(a)), axis = 1)
    return mat

initial = galois.GF2([[]] * 256)
strs = []

old_rank = 0
while True:
    new = random_blk()
    new_mat = gen_mat(strs + [new])
    new_rank = np.linalg.matrix_rank(new_mat)
    print("Trying " + new)
    if new_rank > old_rank:
        print("Rank is now " + str(new_rank))
        strs += [new]
        old_rank = new_rank
        if old_rank == 256:
            break

target_vec = galois.GF2(bytes_2_bits(target))
solution = np.linalg.solve(gen_mat(strs), target_vec)
print(solution)

out = ""
for b,s in zip(solution, strs):
    if b == 1:
        out += s

print(out)

def split_blocks(inp):
    return (inp[i:i+CHUNK_SIZE] for i in range(0, len(inp), CHUNK_SIZE))

def securest_hash(inp):
    blks = split_blocks(inp)
    hashes = [hash_block(blk) for blk in blks]
    result = hashes[0]
    for h in hashes[1:]:
        result = xor(result, h)
    return result

test = securest_hash(out)
print(test.hex())
print(target.hex())
