from hashlib import md5
from sage.all import *
from tqdm import *
from pwn import *
import HashTools
import string


class rod_polse_generator:
    def __init__(self, salt, pepper, meat, size):
        self.salt = salt
        self.pepper = pepper
        self.meat = meat
        self.size = size

    def next_polse(self):
        self.meat = (self.salt * self.meat + self.pepper) % self.size

    def get_polse(self):
        self.next_polse()
        return self.meat


FLAG = b"?" * 46

# io = process(["python3", "./container/service.py"], level="warning")
io = remote("127.0.0.1", 50000, level="warning")

io.recvline()

samples = []
for _ in range(7):
    samples.append(io.recvline().decode()[:-1])

flag_format = b"SSM"
y = b""
for i in range(3):
    for b in range(256):
        guess = y + bytes([b])
        sample = xor(guess, flag_format[: i + 1])
        if md5(sample).hexdigest() == samples[i]:
            y = guess
            break

# LCG paramater recovery, alternatively brute-force
Z = Zmod(2**8)
y0 = Z(y[0])
y1 = Z(y[1])
y2 = Z(y[2])
salt = (y2 - y1) * (y1 - y0) ** -1
pepper = y1 - salt * y0

polse = y
for _ in range(7 - 3):
    polse += bytes([salt * polse[-1] + pepper])

known = b"}SSM{"
for i in range(4, 7):
    for b in range(256):
        guess = known[1:] + bytes([b])
        sample = xor(guess, polse[: i + 1])
        if md5(sample).hexdigest() == samples[i]:
            known += bytes([b])
            break

io.recvline()
io.recvline()

lcg = rod_polse_generator(salt, pepper, polse[-1], 2**8)

payload = bytes([lcg.get_polse() for _ in range(len(FLAG) * 4 - 1)]).hex()
io.sendlineafter(b"\n", payload.encode())
org_sig = io.recvline().decode()[:-1]

data, ext_sig = HashTools.new("md5").extension(
    secret_length=len(FLAG) * 4 - 1,
    original_data=b"",
    append_data=b"\x00",
    signature=org_sig,
)

alph = string.printable
for i in tqdm(range(255)):
    check = False
    for ch in alph:
        b = bytes([i])
        padding = xor(data[:-1], known + b)

        payload = b"\x00" * (len(FLAG) * 4 - 1) + padding + ch.encode()
        polse = bytes([lcg.get_polse() for _ in range(len(payload))])
        payload = xor(payload, polse).hex()

        io.sendlineafter(b"\n", payload.encode())
        sig = io.recvline().decode()[:-1]

        if ext_sig == sig:
            check = True
            known += b
            break

    if check:
        break

flag = b""
for i in tqdm(range(len(FLAG) - len(padding) + 1)):
    _, ext_sig = HashTools.new("md5").extension(
        secret_length=len(FLAG) * 4 - 1,
        original_data=b"",
        append_data=b"\x00" * (i + 1),
        signature=org_sig,
    )
    for ch in alph:
        payload = b"\x00" * (len(FLAG) * 4 - 1) + padding + flag + ch.encode()
        polse = bytes([lcg.get_polse() for _ in range(len(payload))])
        payload = xor(payload, polse).hex()

        io.sendlineafter(b"\n", payload.encode())
        sig = io.recvline().decode()[:-1]

        if ext_sig == sig:
            flag += ch.encode()
            break

print((known[1:] + flag).decode())
