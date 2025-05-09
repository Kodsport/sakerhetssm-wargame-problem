#!/usr/bin/env sage
from sage.all_cmdline import *   # import sage library
from sage.arith.misc import CRT_list
from sage.arith.functions import LCM_list
from sage.combinat.permutation import Permutation
from math import log2
from hashlib import sha256

def get_list(f, v):
    s = f.readline()
    prefix = f"{v} = ["
    assert(s.startswith(prefix))
    assert(s.endswith("]\n"))
    return [int(x) for x in s[len(prefix):-2].split(", ")]

def get_hash(f):
    s = f.readline()
    prefix = f"sha256_1e6(flag) = '"
    assert(s.startswith(prefix))
    assert(s.endswith("'\n"))
    return s[len(prefix):-2].strip()

def sha256_once(b):
    h = sha256()
    h.update(b)
    return h.digest()

def sha256_1e6(b):
    h = b.encode()
    for _ in range(10**6):
        h = sha256_once(h)
    return h.hex()

with open("data.txt", "r") as f:
    g = get_list(f, "g")
    A = get_list(f, "A")
    flag_hash = get_hash(f)

def cycles(p):
    return Permutation([x+1 for x in p]).to_cycles()

def mul(p, q):
    return [q[p[i]] for i in range(N)]

def exp(p, n):
    if n == 0:
        return list(range(N))
    even = exp(mul(p, p), n//2)
    return even if n % 2 == 0 else mul(p, even)

assert len(g) == len(A)
N = len(g)
print(f"{N = }")

g_cycles = cycles(g)
A_cycles = cycles(A)

#print(f"{g_cycles = }")
#print(f"{A_cycles = }")

A_cycles_from_min = {}
for cycle in A_cycles:
    A_cycles_from_min[cycle[0]] = cycle

iter_back_to_start = []
iter_coinciding = []
for cycle in g_cycles:
    if len(cycle) > 1:
        iter_back_to_start.append(len(cycle))
        A_cycle = A_cycles_from_min[cycle[0]]
        iter_coinciding.append(cycle.index(A_cycle[1 % len(A_cycle)]))

print(f"{iter_coinciding = }")
print(f"{iter_back_to_start = }")

secret_remainder = CRT_list(iter_coinciding, iter_back_to_start)
secret_modulus = LCM_list(iter_back_to_start)

print(f"{secret_remainder = }")
print(f"{secret_modulus = }")
print(f"{int(log2(secret_modulus)) = } (bits of `a` determined)")

assert exp(g, secret_modulus) == list(range(N))
assert exp(g, secret_remainder) == A

for i in range(1000):
    secret = int(secret_remainder + i * secret_modulus)
    flag_candidate = f"SSM{{{secret}}}"
    print(f"{flag_candidate = }")
    if sha256_1e6(flag_candidate) == flag_hash:
        flag = flag_candidate
        print(f"{flag = }")
        break
