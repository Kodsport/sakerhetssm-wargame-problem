#!/usr/bin/env python3

from flag import KEY, FLAG
from Crypto.Cipher import AES

assert len(KEY) == 16

solution = f"Here's your flag: {FLAG}. Hope you liked it!".encode()

def bytes_to_binary(b):
    return [(x >> i) & 1 for x in b for i in range(8)]

def similarity(plaintext):
    diffs = [x == y for x, y in zip(bytes_to_binary(plaintext), bytes_to_binary(solution))]
    return sum(diffs) / len(diffs)

if __name__ == "__main__":
    while True:
        cipher = AES.new(KEY, AES.MODE_CBC, iv=KEY)

        print("Please enter data to be decrypted:", flush=False)
        data = bytes.fromhex(input())

        decrypted = cipher.decrypt(data)
        print(f"Your decrypted data is {decrypted.hex()}", flush=False)
        print(f"Your data is {similarity(decrypted)*100}% similar to the solution", flush=True)
