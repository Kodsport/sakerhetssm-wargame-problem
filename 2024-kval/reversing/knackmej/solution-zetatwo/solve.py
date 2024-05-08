#!/usr/bin/env python3

with open('../knackmej', 'rb') as fin:
    fin.seek(0x3020)
    encrypted = fin.read(2*0x22)
decrypted = bytes([x^42 for x in encrypted]).decode()
decoded = bytes.fromhex(decrypted)
flag = bytes([(x-0x1e)&0xFF for x in decoded]).decode()
print(f'Flag: {flag}')
