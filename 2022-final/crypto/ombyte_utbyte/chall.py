#!/usr/bin/env python
from random import shuffle, randint
from hashlib import sha256

N = 100_000

def mul(p, q):
    return [q[p[i]] for i in range(N)]

def exp(p, n):
    if n == 0:
        return list(range(N))
    even = exp(mul(p, p), n//2)
    return even if n % 2 == 0 else mul(p, even)

a = randint(1, 2**64)
g = list(range(N))
shuffle(g)
A = exp(g, a)


def sha256_once(b):
    h = sha256()
    h.update(b)
    return h.digest()
def sha256_1e6(b):
    h = b.encode()
    for _ in range(10**6):
        h = sha256_once(h)
    return h.hex()

flag = f"SSM{{{a}}}"
print(f"{flag = }")

with open("data.txt", "w") as f:
    print(f"{g = }", file=f)
    print(f"{A = }", file=f)
    print(f"{sha256_1e6(flag) = }", file=f)
