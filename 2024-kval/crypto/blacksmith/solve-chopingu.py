from Crypto.Util.number import *
from sage.all import *
from tqdm import *
from pwn import *
import random
import string

io = remote('127.0.0.01', 50000, level='warning')

io.recvuntil(b': ')
public_key = eval(io.recvuntil(b')'))

cnt = 0
while True:
    print(cnt)
    cnt += 1

    m = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    m_val = bytes_to_long(m.encode())

    facts = []
    for fact in list(factor(m_val)):
        for _ in range(fact[1]):
            facts.append(fact[0])

    flag = True
    for i in range(1 << len(facts)):
        m1_val = 1
        for j in range(len(facts)):
            if (i & (1 << j)) != 0:
                m1_val *= facts[j]

        m2_val = m_val // m1_val

        try:
            m1 = long_to_bytes(m1_val).decode('ascii')
            m2 = long_to_bytes(m2_val).decode('ascii')
        except:
            continue

        if m1.isalnum() and m2.isalnum():
            flag = False
            break

    if flag is False:
        break

io.recv()
io.sendline(m.encode())

io.recv()
io.sendline(m1.encode())

io.recv()
io.sendline(m2.encode())

io.recvuntil(b': ')
sig1, sig2 = eval(io.recvuntil(b')'))
io.recv()

sig1 = int(sig1)
sig2 = int(sig2)

io.sendline(str(hex((int(sig1)*int(sig2)) % public_key[1]))[2:].encode())

print(io.recvuntil(b'\n').decode())
