from Crypto.Util.number import *
from sage.all import *
from tqdm import *

with open('autput', 'r') as f:
    autput = int(f.readline())
    n = int(f.readline())
    enc_flag = int(f.readline())
    f.close()

for i in tqdm(range(1, 16)):
    for j in range(1, 16):
        p = var('p')
        sol = solve(i * p**8 - p**3 * autput + j * n**3, p)

        try:
            p = int(sol[0].rhs())
        except:
            continue

        if gcd(p, n) == p: 
            q = n // p 
            phi = (p - 1) * (q - 1)
            e = 0x10001
            d = pow(e, -1, phi)
            flag = pow(enc_flag, d, n)
            print(long_to_bytes(flag).decode())
            exit()
