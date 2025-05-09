#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from hashlib import sha256

from flag import VAULT_PASSWORD


class Ragnars_Runestones:
    def __init__(self):
        self.rsa_key = RSA.generate(2048)
        self.rsa_key_pub = (self.rsa_key.n, self.rsa_key.e)
        self.cipher = AES.new(get_random_bytes(16), AES.MODE_ECB)
        self.rsa_key_enc = self.cipher.encrypt(self.format_rsa_key())
        self.vault_password = VAULT_PASSWORD
        self.vault_password_enc = AES.new(sha256(long_to_bytes(self.rsa_key.p + self.rsa_key.q)).digest(), AES.MODE_ECB).encrypt(pad(VAULT_PASSWORD, 16))

    def format_number(self, num):
        num_bytes = long_to_bytes(num)
        return long_to_bytes(len(num_bytes), 2) + num_bytes

    def format_rsa_key(self):
        s = b""
        s += self.format_number(self.rsa_key.p)
        s += self.format_number(self.rsa_key.q)
        s += self.format_number(self.rsa_key.d)
        s += self.format_number(self.rsa_key.u)
        return pad(s, 16)

    def parse_rsa_key(self, rsa_key):
        idx = 0
        nums = []
        while idx < len(rsa_key):
            l = bytes_to_long(rsa_key[idx : idx + 2])
            idx += 2
            nums.append(bytes_to_long(rsa_key[idx : idx + l]))
            idx += l

        assert len(nums) == 4
        return nums

    # Chinese Remainder Theorem RSA (Garner's formula)
    def rsa_crt_decrypt(self, ct, p, q, d, u):
        ct = bytes_to_long(ct)
        dp = d % (p - 1)
        dq = d % (q - 1)
        mp = pow(ct, dp, p)
        mq = pow(ct, dq, q)
        t = (mq - mp) % q
        h = (t * u) % q
        m = h * p + mp
        return long_to_bytes(m)

    def customer_request(self, request_enc, rsa_key_enc):
        rsa_key = unpad(self.cipher.decrypt(rsa_key_enc), 16)
        p, q, d, u = self.parse_rsa_key(rsa_key)

        runestone_text = self.rsa_crt_decrypt(request_enc, p, q, d, u)
        return runestone_text


store = Ragnars_Runestones()

print("Welcome to my store Ragnar's Runstones!")
print("Here is the rsa key I use: ")
print(f"Public key: {store.rsa_key_pub}")
print(f"Private key: {store.rsa_key_enc.hex()}")
print(
    "To guarantee that my customer service truly is safe I display my encrypted vault password: "
)
print(store.vault_password_enc.hex())

while True:
    print(
        "When you have decided what to order, give me your encrypted request and the corresponding private key."
    )

    request_enc = bytes.fromhex(input("Request: "))
    rsa_key_enc = bytes.fromhex(input("Rsa_key: "))

    runestone = store.customer_request(request_enc, rsa_key_enc)

    print(f"Here is your beautiful runestone: {runestone.hex()}")
