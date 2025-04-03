#!/usr/bin/env python3

from Crypto.Random.random import getrandbits
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad
from collections import namedtuple
from hashlib import sha256, md5
from Crypto.Cipher import AES
from flag import FLAG

# https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
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


# NIST P-256 curve
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
G = Point(
    0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)

# https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
Hellman_privkey = getrandbits(128)
Diffie_privkey = getrandbits(128)

while True:
    print("=======================================")
    print("Initiating Hellman & Diffie protocol...")
    print("=======================================")
    print("= Curve: NIST P-256")
    print("=======================================")
    print("= Ephemeral key size: 128")
    print("=======================================")
    print("= Shared key hash: MD5")
    print("=======================================")
    print("= Confirmation hash: SHA-256")
    print("=======================================")
    print("= Agree on a generator: ")

    gx = int(input("= gx: "), 16)
    gy = int(input("= gy: "), 16)
    Gen = Point(gx, gy)

    print("=======================================")
    print("= Generator chosen: ")
    print(f"= {str(Gen)}")
    print("=======================================")
    print("= Hellman please send your public key")

    Hellman_pubkey = double_and_add(Gen, Hellman_privkey)

    print("=======================================")
    print("= Hellman to Diffie: ???")
    print("=======================================")
    print("= Diffie please send your public key")

    Diffie_pubkey = double_and_add(Gen, Diffie_privkey)

    print("=======================================")
    print("= Diffie to Hellman: ???")
    print("=======================================")
    print("= Hellman please send confirmation hash")
    print("=======================================")
    print("= Hellman to protocol: ")

    Hellman_shared_secret = double_and_add(Diffie_pubkey, Hellman_privkey)
    Hellman_confirmation_hash = sha256(str(Hellman_shared_secret).encode()).hexdigest()

    print(Hellman_confirmation_hash)

    print("=======================================")
    print("= Diffie please send confirmation hash")
    print("=======================================")
    print("= Diffie to protocol: ")

    Diffie_shared_secret = double_and_add(Hellman_pubkey, Diffie_privkey)
    Diffie_confirmation_hash = sha256(str(Diffie_shared_secret).encode()).hexdigest()

    print(Diffie_confirmation_hash)

    print("=======================================")
    print("= Confirmed. Send messages now")
    print("=======================================")
    print("= Hellman to Diffie: ")

    Hellman_message = (
        b"Send me the key to the new fashion style that will earn us millions Diffie!"
    )
    key = md5(str(Hellman_shared_secret).encode()).digest()
    Hellman_enc_message = AES.new(key, AES.MODE_ECB).encrypt(pad(Hellman_message, 16))

    print(Hellman_enc_message.hex())

    print("=======================================")
    print("= Diffie to Hellman: ")

    if Gen == G:
        Diffie_message = FLAG
    else:
        Diffie_message = b"SHhhh!!!! I think someone is listening in on us..."

    key = md5(str(Diffie_shared_secret).encode()).digest()
    Diffie_enc_message = AES.new(key, AES.MODE_ECB).encrypt(pad(Diffie_message, 16))

    print(Diffie_enc_message.hex())

    print("=======================================")
    print("= Closing protocol...")
    print("=======================================")
    print()
