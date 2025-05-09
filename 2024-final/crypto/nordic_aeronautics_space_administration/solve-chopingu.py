from collections import namedtuple
from sage.all import *
from tqdm import *

Point = namedtuple("Point", "x y")
O = "Origin"


def point_inverse(P):
    if P == O:
        return P

    return Point(P.x, -P.y % p)


def point_addition(P, Q, stage):
    if stage == "Big":
        a = a1
        b = b1
    elif stage == "Bang":
        a = a2
        b = b2

    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3 * P.x**2 + a) * inverse_mod(2 * P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse_mod((Q.x - P.x), p)
            lam %= p

    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam * (P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)

    return R


def double_and_add(P, n, stage):
    if stage == "Big":
        a = a1
        b = b1
    elif stage == "Bang":
        a = a2
        b = b2

    Q = P
    R = O
    while n > 0:
        if n & 1 == 1:
            R = point_addition(R, Q, stage)
        Q = point_addition(Q, Q, stage)
        n = n // 2

    return R


def translate(P):
    return Point(P[0] + sing_root, P[1])


def homomorphism_1(P):
    x, y = P
    return (y + qr * x) * inverse_mod(y - qr * x, p) % p


def homomorphism_2(P):
    x, y = P
    return GF(p)(x) / GF(p)(y)


p = 4368590184733545720227961182704359358435747188309319510520316493183539079703

Big = Point(
    8742397231329873984594235438374590234800923467289367269837473862487362482,
    225987949353410341392975247044711665782695329311463646299187580326445253608,
)

Bang = Point(
    3543222481423432511601699147997255185824699912464451488875339984288911042103,
    408303939746921587627140516874478355186777376615263734855495089378228650923,
)

with open("hydrogen", "r") as f:
    hydrogen = eval(f.read())
    f.close()

with open("helium", "r") as f:
    helium = eval(f.read())
    f.close()

# calculate curve parameters
G = Big
Q = hydrogen[0]
a1 = (
    ((G[1] ** 2 - G[0] ** 3) - (Q[1] ** 2 - Q[0] ** 3)) * inverse_mod((G[0] - Q[0]), p)
) % p
b1 = (G[1] ** 2 - G[0] ** 3 - a1 * G[0]) % p

G = Bang
Q = helium
a2 = (
    ((G[1] ** 2 - G[0] ** 3) - (Q[1] ** 2 - Q[0] ** 3)) * inverse_mod((G[0] - Q[0]), p)
) % p
b2 = (G[1] ** 2 - G[0] ** 3 - a1 * G[0]) % p


# translate singular point of curve
x = GF(p)["x"].gen()
f = x**3 + a1 * x + b1
sing_root = f.factor()[1][0][0]
f_ = f.subs(x=x - sing_root)
qr = mod(f_.factor()[0][0][0], p).sqrt()

# solve dlog using homomorphism to small group
protons = []
Big_ = homomorphism_1(translate(Big))
for i in tqdm(range(len(hydrogen))):
    hydrogen_atom = homomorphism_1(translate(hydrogen[i]))
    protons.append(discrete_log(hydrogen_atom, Big_, operation="*"))

# LLL to get flag chars using second homorphism
n = len(protons)
m = matrix(ZZ, n + 2, n + 2)
m[n, n + 1] = (2**256) * homomorphism_2(helium)
for i in range(n + 1):
    m[i, i] = 1
    if i != n:
        m[i, n + 1] = (2**256) * homomorphism_2(
            double_and_add(Bang, protons[i] * protons[i], "Bang")
        )

m[n + 1, n + 1] = p

lll = m.LLL()
for sol in lll:
    if sol[-1] != 0:
        continue

    mult = 1
    if sol[0] == -ord("S"):
        mult = -1

    for val in sol:
        try:
            print(chr(mult * val), end="")
        except:
            continue

print()
