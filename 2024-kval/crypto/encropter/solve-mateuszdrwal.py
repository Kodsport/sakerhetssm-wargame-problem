from pwn import *
from randcrack import RandCrack

conn = remote("127.0.0.1", 50000)
rc = RandCrack()

for i in range(624):
    conn.sendline(b"0")
    conn.recvuntil(b"Encropted: ")
    rc.submit(int(conn.recvline()))

conn.sendline()
conn.recvuntil(b"SSM{")
resp = conn.recvuntil(b"}")[:-1]

print("SSM{", end="")
print(int(resp[: len(resp) // 2]) ^ rc.predict_getrandbits(32), end="")
print(int(resp[len(resp) // 2 :]) ^ rc.predict_getrandbits(32), end="")
print("}", end="")
