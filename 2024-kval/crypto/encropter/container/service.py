#!/usr/bin/env python3.9

from FLAG import FLAG

import random

print(
"""Welcome to my encroption service!
You can encropt any number of integers!

Enter integer to encropt:"""
)

while True:
    input_string = input()

    if not input_string:
        break

    plain = int(input_string)
    key = random.getrandbits(32)
    cipher = plain ^ key
    print("Encropted:", cipher)
    print("Enter integer to encropt:")

print("To verify that the encroption is correct, I will now send you a Super Secure Message:")

FLAG = FLAG.removeprefix("SSM{").removesuffix("}")
FLAG1, FLAG2 = int(FLAG[:len(FLAG)//2]), int(FLAG[len(FLAG)//2:])

FLAG1 = str(random.getrandbits(32) ^ FLAG1)
FLAG2 = str(random.getrandbits(32) ^ FLAG2)

print("SSM{" + FLAG1 + FLAG2 + "}")
