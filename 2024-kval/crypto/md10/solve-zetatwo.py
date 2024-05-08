#!/usr/bin/env python3

import string
import hashlib
import itertools

with open('enc_flag', 'r') as fin:
    enc_flag = int(fin.read().strip())
    
lookup = {}

#ALPHA = string.ascii_uppercase + string.ascii_lowercase + string.digits + '_-'
ALPHA = string.printable

part_b = '_gu3ss_y0u_l1ttl3...}'
part_a = 'SSM{d0nt_3v3n_try_t0_'

print('Building lookup')
for cand in itertools.product(ALPHA, repeat=3):
    cand_str = ''.join(cand) + part_b
    assert len(cand_str) == 24
    b = int(hashlib.md5(cand_str.encode()).hexdigest(), 16)
    lookup[b] = cand


print('Looking up')
for cand in itertools.product(ALPHA, repeat=4):
    cand_str = part_a + ''.join(cand)
    assert len(cand_str) == 25
    a = int(hashlib.md5(cand_str.encode()).hexdigest(), 16)

    diff = enc_flag - a
    b = lookup.get(diff, None)
    if b != None:
        print(f"Flag: {part_a}{''.join(cand)}{''.join(b)}{part_b}")
        break
