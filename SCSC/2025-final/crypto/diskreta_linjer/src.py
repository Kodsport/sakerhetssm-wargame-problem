from Crypto.Util.number import *
from sage.all import *
from flag import FLAG


assert len(FLAG) == 15 * 5
assert FLAG[:5] == b"SNHT{"


p = getPrime(2048)
print(p)


F = GF(p)


class Line:
    k0 = None
    m = F(randint(0, p - 1))
    def __init__(self):
        self.k = F(randint(0, p - 1))
        self.m = Line.m

    def __call__(self, x):
        return self.k * x + self.m
    
    def __repr__(self):
        return f"{Line.k0 / self.k}" #f"{self.k} * x + {self.m}"


otp_key = [F(randint(0, p - 1)) for _ in range(5)]


for i in range(15):
    line = Line()

    if i == 0:
        Line.k0 = line.k

    chs = [((getrandbits(92) << 8) ^ FLAG[i * 5 + j]) for j in range(5)]
    enc_chs = [(otp * chunk) for otp, chunk in zip(otp_key, chs)]

    print(f"{line}, {line(sum(enc_chs))}")
