import random

from pwn import *
from randcrack import RandCrack

r = remote("localhost", 50000)

cracker = RandCrack()

for i in range(624):
    r.recvuntil(b"Enter integer to encropt:\n")
    nmbr = random.getrandbits(32)
    r.sendline(str(nmbr).encode())
    r.recvuntil(b"Encropted: ")
    encropted = int(r.recvline().decode())
    gen_bits = encropted ^ nmbr
    cracker.submit(gen_bits)

r.sendline()
r.recvuntil(b"Message:\n")
encropted_flag = r.recvline().decode().removeprefix("SSM{").removesuffix("}\n")
half = len(encropted_flag)//2
flag1, flag2 = int(encropted_flag[:half]), int(encropted_flag[half:])
flag1 = flag1 ^ cracker.predict_getrandbits(32)
flag2 = flag2 ^ cracker.predict_getrandbits(32)

print("SSM{" + str(flag1) + str(flag2) + "}")

r.interactive()
