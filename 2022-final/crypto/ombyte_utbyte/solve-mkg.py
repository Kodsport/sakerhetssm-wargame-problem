#!/usr/bin/env python3
from functools import reduce
from hashlib import sha256
import math, sympy

def chinese_remainder(n, a):
    # https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
    s = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        s += a_i * pow(p, -1, n_i) * p
    return s % prod

N = 100_000
def mul(p, q):
    return [q[p[i]] for i in range(N)]
def sha256_once(b):
    h = sha256()
    h.update(b)
    return h.digest()
def sha256_1e6(b):
    h = b.encode()
    for _ in range(10**6):
        h = sha256_once(h)
    return h.hex()

with open("data.txt") as f:
    # what?? I'm lazy!
    g = eval(f.readline()[4:])
    A = eval(f.readline()[4:])

modulos = [-1]*N
rests = [-1]*N
p = list(range(N))
for i in range(1, N+1):
    if i % 10000 == 0:
        print(i)
    p = mul(p, g)
    for j in range(N):
        if modulos[j] == -1 and p[j] == j:
            modulos[j] = i
        if rests[A[j]] == -1 and p[j] == A[j]:
            rests[A[j]] = i

assert all([x != -1 for x in modulos])
assert all([x != -1 for x in rests])

combo = list(set(zip(modulos, rests)))
combo.sort(reverse=True)

Nprod = 1
Ns = []
As = []
a_size = 2**64
for (i, (m, r)) in enumerate(combo):
    factors = list(sympy.factorint(m).keys())
    for f in factors:
        if math.gcd(Nprod, f) != 1:
            continue

        Nprod *= f
        Ns.append(f)
        As.append(r % f)
        print(i, f, Nprod, Nprod/a_size)
        if Nprod > a_size:
            break
    if Nprod > a_size:
        break
assert Nprod > a_size

a = chinese_remainder(Ns, As)
flag = f"SSM{{{a}}}"
print(f"{flag = }")
shaflag = sha256_1e6(flag)
print(shaflag)

sha1e6flag = "9073ea1547e9a87dbb58be9db35135ff3468870575e5544a59fd4dda5499f349"
assert shaflag == sha1e6flag
