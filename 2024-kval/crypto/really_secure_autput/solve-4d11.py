"""
autput = R1 * (n/q)**5 + R2 * q**3
= R1 * n**5 * q**-5 + R2 * q**3

autput * q**5 = R1 * n**5 + R2 * q**8

0 = (R1 * n**5) + (R2 * q**8) - (autput * q**5)
"""
from sage.all import *

with open("autput", "r") as file:
    autput, n, c = map(int, file.read().split())


found = False

for R1 in range(1, 17):
    for R2 in range(1, 17):
        q = var("q")
        res = solve((R1 * n**5) + (R2 * q**8) - (autput * q**5), q)
        if len(res) != 1:
            q_val = res[0]
            found = True
            break
    if found:
        break

q = int(q_val.rhs())

p = n//q

d = pow(0x10001, -1, (p-1)*(q-1))

m = pow(c, d, n)

from Crypto.Util.number import long_to_bytes

print(long_to_bytes(m))
