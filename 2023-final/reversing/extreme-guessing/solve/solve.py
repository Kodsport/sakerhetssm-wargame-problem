import sys
import pwn

from xorshift_crack import xorshift128_n, find_st, to_double

s = pwn.remote(sys.argv[1], int(sys.argv[2]), ssl=True)

def play(n):
    header = s.recvline()
    s.send(b'J\n')
    tänker = s.recvline()
    s.send(f'{n}\n'.encode())
    got = s.recvline().strip()
    if got in ("För högt!".encode(), "För lågt!".encode()):
        high = got == "För lågt!".encode()
        loss = s.recvline()
        return high
    elif got.startswith(b"Du vann"):
        pwn.log.success(got.decode(errors="replace"))
    else:
        pwn.log.error(got)
        exit()

bits_got = []

with pwn.log.progress("Gathering data") as pr:
    for i in range(2):
        chunk = []
        for j in range(64):
            pr.status(f"{i*64+j}/128")
            chunk.append(play(0.5))
        bits_got.extend(chunk[::-1])

st = find_st(bits_got)

# regenerate all numbers we've already got
for i in range(128):
    n = to_double(st[0])
    assert (n > 0.5) == bits_got[i]
    st = xorshift128_n(*st)

next_64_numbers = []

for _ in range(64):
    next_64_numbers.append(to_double(st[0]))
    st = xorshift128_n(*st)

next_64_numbers = next_64_numbers[::-1]
next_number = next_64_numbers[0]
play(next_number)
