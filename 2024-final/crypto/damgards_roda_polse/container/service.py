#!/usr/bin/env python3

from Crypto.Random.random import *
from Crypto.Util.number import *
from itertools import cycle
from hashlib import md5

from flag import MUSTARD


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


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


# 3 bit primes for moderate amount of seasoning
salt = getPrime(3)
pepper = getPrime(3)
meat = getPrime(3)
size = 2**8
damgards_roda_polse = rod_polse_generator(salt, pepper, meat, size)

sample_polse = bytes([damgards_roda_polse.get_polse() for _ in range(7)])

print("Welcome to my Damgards Polse! Here is a small sample of our famous product:")
for i in range(7):
    sample = xor(cycle(MUSTARD), sample_polse[: i + 1])
    print(md5(sample).hexdigest())

print("Did you enjoy it? If so, feel free to buy as many polse as you want!")
print(
    f"I will put {len(MUSTARD)} cm of mustard on the polse for extra tastiness, but you can always add extra toppings!!! "
)

while True:
    print("What extra toppings do you want?")
    try:
        topping = bytes.fromhex(input())
    except:
        print("Invalid topping :(")
        exit()

    if len(topping) < len(MUSTARD):
        print("The mustard will overpower your topping with that amount...")
        exit()

    polse = [damgards_roda_polse.get_polse() for _ in range(len(topping))]
    polse_with_mustard = xor(cycle(MUSTARD), polse)
    polse_with_toppings = xor(polse_with_mustard, topping)

    print(md5(polse_with_toppings).hexdigest())
