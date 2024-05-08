from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from hashlib import sha256
from pwn import *


class BinarySearch:
    def __init__(self, pubk, bruteforce_threshold=(1 << 20)):
        self.n, self.e = pubk
        self.oracle_queries = 0

        self.lo = 1 << (self.n.bit_length() // 2 - 1)
        self.hi = (1 << ((self.n.bit_length() + 1) // 2)) - 1

        self.bruteforce_threshold = bruteforce_threshold

    def next(self):
        mid = (self.lo + self.hi) >> 1
        self.last_mid = mid

        ct = pow(mid, self.e, self.n)

        return long_to_bytes(ct)

    def query(self, r):
        self.oracle_queries += 1

        if (r - self.last_mid) % self.n == 0:
            self.lo = self.last_mid
        else:
            self.hi = self.last_mid

        q = 1
        if self.hi - self.lo > self.bruteforce_threshold:
            return False
        else:
            for q in range(self.lo, self.hi + 1):
                if self.n % q == 0:
                    break

        if q == 0:
            assert False, "No root found"

        p = self.n // q

        assert 1 < p < self.n
        assert self.n == p * q

        self.p = p
        self.q = q

        return True


# io = process(["python3", "./container/service.py"], level="warning")
io = remote("127.0.0.1", 50000, level="warning")

io.recvuntil(b"Public key: ")
rsa_key_pub = eval(io.recvline().decode())
io.recvuntil(b"Private key: ")
rsa_key_enc = bytearray(bytes.fromhex(io.recvuntil(b"\n")[:-1].decode()))

io.recvline()
vault_password_enc = bytes.fromhex(io.recvline()[:-1].decode())

# garble u
l = len(rsa_key_enc)
rsa_key_enc[l - 2 * 16 : l - 16] = xor(rsa_key_enc[l - 2 * 16 : l - 16], b"a" * 16)

binsearch = BinarySearch(rsa_key_pub)
print("## Running binary search, recovered bits:    0", end="")
while True:
    ct = binsearch.next()

    io.sendlineafter(b"Request: ", ct.hex().encode())
    io.sendlineafter(b"Rsa_key: ", rsa_key_enc.hex().encode())

    io.recvuntil(b": ")
    r = int(io.recvuntil(b"\n")[:-1].decode(), 16)

    if binsearch.query(r):
        p = binsearch.p
        q = binsearch.q
        key = sha256(long_to_bytes(p + q)).digest()

        print("\n" + AES.new(key, AES.MODE_ECB).decrypt(vault_password_enc).strip(b'\x07').decode())
        exit()

    recovered_bits = str(binsearch.oracle_queries).rjust(4)
    print(f"\r## Running binary search, recovered bits: {recovered_bits}", end="")
