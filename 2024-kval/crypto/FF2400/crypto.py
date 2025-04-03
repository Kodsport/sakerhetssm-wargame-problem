import random
from string import ascii_uppercase

def generate_key():
    key = list(ascii_uppercase)
    random.shuffle(key)
    key = "".join(key)
    return key

def encrypt(msg, key):
    msg = msg.upper()
    ciphertext = ""
    for char in msg:
        if char in key:
            i = key.index(char)
            ciphertext += ascii_uppercase[i]
        else:
            ciphertext += char
    return ciphertext

def decrypt(cph, key):
    cph = cph.upper()
    plaintext = ""
    for char in cph:
        if char in ascii_uppercase:
            i = ascii_uppercase.index(char)
            plaintext += key[i]
        else:
            plaintext += char
    return plaintext

if __name__ == "__main__":
    key = generate_key()
    with open("key.txt", "w") as file:
        file.write(key)
    with open("plaintext.txt") as file:
        plaintext = file.read()
    ciphertext = encrypt(plaintext, key)
    with open("ciphertext.txt", "w") as file:
        file.write(ciphertext)
