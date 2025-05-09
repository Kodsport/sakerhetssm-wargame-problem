from itertools import product
from string import printable
from hashlib import md5
from tqdm import *

with open('enc_flag', 'r') as f:
    a_b = int(f.read())
    f.close()

a = b'SSM{d0nt_3v3n_try_t0_'
b = b'_gu3ss_y0u_l1ttl3...}'

ltable = {}

perms = list(product(printable, repeat = 3))
for i in tqdm(range(len(perms))):
    b_guess = ''.join(perms[i]).encode() + b
    b_val = int(md5(b_guess).hexdigest(), 16)
    ltable[b_val] = b_guess

perms = list(product(printable, repeat = 4))
for i in tqdm(range(len(perms))):
    a_guess = a + ''.join(perms[i]).encode()
    a_val = int(md5(a_guess).hexdigest(), 16)
    
    b_val = a_b - a_val
    if b_val in ltable:
        print((a_guess + ltable[b_val]).decode())
        exit()
