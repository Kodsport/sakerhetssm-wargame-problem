#!/usr/bin/env python3

import random
import sys

if len(sys.argv) < 2:
    print('Usage: generate.py <seed>')
    sys.exit(1)

random.seed(sys.argv[1])

sbox = list(range(256))
random.shuffle(sbox)

print('#include "parameters.hpp"')

sbox_str = ', '.join(f'{x:#04x}' for x in sbox)
print(f'const uint8_t SBOX[] __attribute__((aligned(16))) = {{ {sbox_str} }};')

indices1 = list(range(64))
random.shuffle(indices1)
mask1 = 0
for i in indices1[:32]:
    mask1 |= (1<<i)
print(f'const uint64_t mask1 = {mask1:#066b};')

indices2 = list(range(64))
random.shuffle(indices2)
mask2 = 0
for i in indices2[:32]:
    mask2 |= (1<<i)
print(f'const uint64_t mask2 = {mask2:#066b};')

key = random.randbytes(16)
key_str = ', '.join(f'{x:#04x}' for x in key)
print(f'const uint8_t KEY[] __attribute__((aligned(16))) = {{ {key_str} }};')
