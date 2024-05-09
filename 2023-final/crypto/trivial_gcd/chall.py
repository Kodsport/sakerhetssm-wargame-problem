from secrets import randbits
from flag import FLAG

def is_prime(p):
    for n in range(2, 15):
        if pow(n, p-1, p) != 1:
            return False
    return True

def next_prime(n):
    while not is_prime(n):
        n += 1
    return n

p = next_prime(randbits(128))
q = next_prime(randbits(128))
r = next_prime(randbits(128))
m = randbits(250)
e_1 = randbits(36)
e_2 = randbits(36)

c_1 = pow(m, e_1, p*q)
c_2 = pow(m, e_2, p*r)

message = int.from_bytes(FLAG.encode(), "little")
cipher = pow(message, 2**16 + 1, p**10)

with open("data.txt", "w") as f:
    print(f"{m = }", file=f)
    print(f"{e_1 = }", file=f)
    print(f"{e_2 = }", file=f)
    print(f"{c_1 = }", file=f)
    print(f"{c_2 = }", file=f)
    print(f"{cipher = }", file=f)
