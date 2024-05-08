#!/usr/bin/env python3

import hashlib
import string

hashes = []
with open('chall.txt', 'r') as fin:
    for line in fin:
        hashes.append(line.strip())

flag = []
for target in hashes:
    for cand in string.printable:
        h = hashlib.md5(cand.encode()).hexdigest()
        if h == target:
            flag.append(cand)
            break
    else:
        print(f'Unknown hash: "{target}"')
        break

print(''.join(flag))
