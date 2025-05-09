from sage.all import *
from tqdm import *

with open('modulus', 'r') as f:
    n = int(f.read())
    Z = Zmod(n)
    f.close()

with open('ai_weights', 'r') as f:
    tmp = eval(f.read())
    weights = [matrix(Z, tmp[i]) for i in range(len(tmp))]
    f.close()

with open('ai_biases', 'r') as f:
    tmp = eval(f.read())
    biases = [matrix(Z, tmp[i]) for i in range(len(tmp))]
    f.close()

with open('enc_flag', 'r') as f:
    enc_flag = matrix(Z, eval(f.read()))
    f.close()

e = 0x100
flag_len = len(*enc_flag)

A = prod(weights)
b = zero_matrix(Z, 1, flag_len)
cur = identity_matrix(Z, flag_len)
for i in range(len(biases)-1, -1, -1):
    b += biases[i] * cur
    cur = weights[i] * cur

cur = identity_matrix(Z, flag_len)
for i in tqdm(range(e)):
    enc_flag -= b*cur
    cur *= A

flag = enc_flag * cur**-1
for ch in list(*flag):
    print(chr(ch), end='')

print()
