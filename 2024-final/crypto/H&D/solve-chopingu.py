from Crypto.Util.number import inverse
from Crypto.Util.Padding import unpad
from collections import namedtuple
from hashlib import sha256, md5
from Crypto.Cipher import AES
from sage.all import *
from tqdm import *
from pwn import *

Point = namedtuple("Point", "x y")
O = "Origin"


def point_inverse(P):
    if P == O:
        return P

    return Point(P.x, -P.y % p)


def point_addition(P, Q):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3 * P.x**2 + a) * inverse(2 * P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p

    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam * (P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)

    return R


def double_and_add(P, n):
    Q = P
    R = O
    while n > 0:
        if n & 1 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2

    return R


def find_subgroups():
    factors = prod(primes(2**15))
    b = 0
    full_order = 1
    curves = []
    while full_order < 2**256:
        print(Integer(full_order).nbits())
        try:
            E = EllipticCurve(GF(p), [a, b])
            o = E.order()
            g = gcd(factors, o)
            l = lcm(g, full_order)
            if l > full_order:
                full_order = l
                curves.append((E, o))
        except:
            pass

        b += 1

    return curves, full_order


def interact(x, y):
    io.recvuntil(b"generator: \n")

    io.recvuntil(b": ")
    io.sendline(hex(x).encode())
    io.recvuntil(b": ")
    io.sendline(hex(y).encode())

    io.recvuntil(b"protocol: \n")
    conf_hash = io.recvline()[:-1].decode()

    io.recvuntil(b"Hellman: \n")
    enc_flag = io.recvline()[:-1].decode()

    return conf_hash, enc_flag


def congruence(G, order, fac):
    A = G * (order // fac)

    x = A.xy()[0]
    y = A.xy()[1]
    conf_hash, _ = interact(x, y)

    P = Point(x, y)
    for i in range(fac):
        Q = double_and_add(P, i)
        conf_hash_guess = sha256(str(Q).encode()).hexdigest()
        if conf_hash_guess == conf_hash:
            return i

    return -1


p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC

curves, full_order = find_subgroups()
factored = {fac: -1 for fac in factor(full_order)}

# io = process(["python3", "./container/service.py"], level="warning")
io = remote("127.0.0.1", 50000, level="warning")


for i in tqdm(range(len(curves))):
    curve, order = curves[i]
    G = curve.gens()[0]
    small_order = gcd(full_order, order)
    for fac in factor(small_order):
        if fac in factored and factored[fac] == -1:
            factored[fac] = congruence(G, order, fac[0])

n = list(map(lambda x: x[0], factored.keys()))
c = list(factored.values())
privkey = crt(c, n)

G = Point(
    0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)
_, enc_flag = interact(*G)
shared_secret = double_and_add(G, privkey)
key = md5(str(shared_secret).encode()).digest()
flag = unpad(AES.new(key, AES.MODE_ECB).decrypt(bytes.fromhex(enc_flag)), 16).decode()

print(flag)
