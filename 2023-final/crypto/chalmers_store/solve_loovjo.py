import pwn, sys

# hash_once(X + Y, m[0]) = hash_once(X, m[0]) + m[0] ** n * hash_once(Y, m[0])
# if hash_once(X) == hash_once(Y), then any equal length concatenations of X and Ys will give the same hash
#
# we find a collision for magic[0] by birthday paradox, takes sqrt(0x1ffff7) attempts.
# we construct collisions for magic[1] by concatenating the previously found collisions
# etc.

import random

def pick_powerset(bases, n):
    out = ""
    for i in range(n):
        out += random.choice(bases)

    return out

magic = [4404 ^ 3214, 25954 ^ 3214, 17763 ^ 3124]
mod = 0x1ffff7

def hashonce(s, b):
    h = 0
    m = 1
    for c in s:
        h += ord(c) * m
        m *= b
        h %= mod
        m %= mod
    return h

def powerhash(s):
    return hashonce(s, magic[0]) + (hashonce(s, magic[1]) << 21) + (hashonce(s, magic[2]) << 42)


# bases = collisions for previous step
def search_collisions(bases, b, n):
    found = {} # {hash: str}
    with pwn.log.progress(f"Searcing {hex(b)}") as prg:
        while True:
            x = pick_powerset(bases, n)
            h = hashonce(x, b)
            if h in found and found[h] != x:
                return x, found[h]
            found[h] = x
            prg.status(f"{len(found)}/{int(mod ** 0.5)}")

b0 = search_collisions("mjau", magic[0], 21)
b1 = search_collisions(b0, magic[1], 21)
b2 = search_collisions(b1, magic[2], 21)
print(f"found collision: {b2[0][:20]}... === {b2[1][:20]}... (len {len(b2[0]), len(b2[1])}")

r = pwn.remote(sys.argv[1], int(sys.argv[2]), ssl=True)

def sell(x):
    r.send(b"1\n")
    r.send(x.encode() + b"\n")

sell(b2[0])
sell(b2[1])
# we now have 600 coins. need to sell 3 random things
sell("cattwo")
sell("catthree")
sell("catfour")

# buy flag
r.send(b"2\nFlag\n3\n")
r.interactive()
