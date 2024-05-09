#!/usr/bin/env python3
from Crypto.Cipher import AES
key = bytes([171,71,22,124,106,110,80,106,104,119,209,28,177,225,32,229])
f = b"SSM{J4g_h4r_3n_plan!_V1_beh0v3r_3n_plansk155_over_arl4nda......}"
aes = AES.new(key, AES.MODE_ECB)
for i in range(0, len(f), 16):
    c = aes.decrypt(f[i:i+16])
    for j in range(16):
        print("\\x" + bytes([c[j]]).hex(), end="")
    print("")
