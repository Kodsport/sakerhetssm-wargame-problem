#!/usr/bin/env python3
from pwn import *
import string
import random
import tqdm

r = remote("127.0.0.1", 50000)
def decrypt(data):
    r.recvline()
    r.sendline(bytes(data.hex(), "ascii"))
    decr = bytes.fromhex(str(r.recvline(), "ascii")[len("Your decrypted data is "):])
    similarity = float(str(r.recvline(), "ascii")[len("Your data is "):].split("%")[0])
    return (decr, similarity)

data = "Here's your flag: "
print(len(data))

cur_guess = b""
similarity = 0
testdata = b"\x00" * 16

similarity = 0

for blk in range(16):
    for i in range(16):
        best_guess = 0
        for j in tqdm.trange(0x100):
            test = b"\x00" * (len(cur_guess)) + bytes([j])
            test += b"\x00" * ((blk+1)*16 - len(test))
            test += testdata
            #print(test)
            decr, test_sim = decrypt(test)
            _, baseline_sim = decrypt(test[:(blk+1) * 16])
            new_sim = ((blk+2)*test_sim - (blk+1)*baseline_sim)
            if (new_sim >= similarity):
                similarity = new_sim
                #print(f"New best: ({new_sim}) {decr}")
                best_guess = decr[16 + len(cur_guess)]
        cur_guess += bytes([best_guess])
        similarity = 0
        try:
            print((cur_guess).decode("utf-8"))
            if (cur_guess[2:].startswith(b"SSM{") and cur_guess.endswith(b"}")):
                print(f"Flag: {(cur_guess).decode('utf-8')[2:]}", flush=True)
                exit(0)
        except:
            pass
