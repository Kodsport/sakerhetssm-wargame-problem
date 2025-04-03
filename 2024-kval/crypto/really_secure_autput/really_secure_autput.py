from Crypto.Util.number import *
from random import randint
from flag import FLAG

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001

m = bytes_to_long(FLAG)
c = pow(m, e, n)

autput = randint(1, 2^18) * p**5 + randint(1, 2^18) * q**3

with open('autput', 'w') as f:
    f.write(str(autput) + '\n')
    f.write(str(n) + '\n')
    f.write(str(c))
    f.close()
