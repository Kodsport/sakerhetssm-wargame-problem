#!/usr/bin/env python3

import sys


input_file = sys.argv[1]

with open(input_file, 'rb') as fin:
    plaintext = fin.read()

key = 0x41
ciphertext = bytes(x^key for x in plaintext)

sys.stdout.buffer.write(ciphertext)
