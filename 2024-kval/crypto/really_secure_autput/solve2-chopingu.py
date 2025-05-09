from Crypto.Util.number import *
from sage.all import *
from gmpy2 import iroot

with open('autput', 'r') as f:
    autput = int(f.readline())
    n = int(f.readline())
    enc_flag = int(f.readline())
    f.close()

for i in range(1, 16):
    p = iroot(autput // i, 5)[0]
    if gcd(n, p) == p:
        q = n // p
        phi = (p - 1) * (q - 1)
        e = 0x10001
        d = pow(e, -1, phi)
        flag = pow(enc_flag, d, n)
        print(long_to_bytes(flag).decode())
        exit()
