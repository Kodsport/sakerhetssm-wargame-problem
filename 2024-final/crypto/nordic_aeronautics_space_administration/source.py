from Crypto.Random.random import getrandbits
from Crypto.Util.number import inverse
from collections import namedtuple
from secret import a1, b1, a2, b2
from flag import FLAG

# https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
# y**3 = x**3 + a*x + b
Point = namedtuple("Point", "x y")
O = "Origin"


# Additive inverse of curve point P
def point_inverse(P):
    if P == O:
        return P

    return Point(P.x, -P.y % p)


# Adding two curve points P and Q
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
            lam = (3 * P.x**2 + a) * inverse(2 * P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p

    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam * (P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)

    return R


# Curve point P multiplied by n
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


# Define field for curves
p = 4368590184733545720227961182704359358435747188309319510520316493183539079703

# Define one curve point
Big = Point(
    8742397231329873984594235438374590234800923467289367269837473862487362482,
    225987949353410341392975247044711665782695329311463646299187580326445253608,
)

# Define another curve point
Bang = Point(
    3543222481423432511601699147997255185824699912464451488875339984288911042103,
    408303939746921587627140516874478355186777376615263734855495089378228650923,
)

protons = [getrandbits(128) for _ in range(len(FLAG))]
neutrons = [quark for quark in FLAG]

hydrogen = []
for i in range(len(FLAG)):
    singular_hydrogen_atom = double_and_add(Big, protons[i], "Big")
    hydrogen.append(singular_hydrogen_atom)

helium = O
for i in range(len(FLAG)):
    cool_physics = double_and_add(Bang, protons[i], "Bang")
    singular_helium_atom = double_and_add(
        cool_physics, protons[i] * neutrons[i], "Bang"
    )
    helium = point_addition(helium, singular_helium_atom, "Bang")

with open("hydrogen", "w") as f:
    f.write(str(hydrogen))
    f.close()

with open("helium", "w") as f:
    f.write(str(helium))
    f.close()
