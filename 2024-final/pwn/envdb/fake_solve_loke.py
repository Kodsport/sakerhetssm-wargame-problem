# This solution attempts to get a timeout with a linear time copy of large string
# This should fail
MAX_LEN = 1e6
N = int(MAX_LEN * 0.5)

def pad(i):
    s = str(i)
    return (5-len(s))*"0" + s

payload0 = "GET FLAG" + "\n"
payload1 = "GET FLAG;SET " + "a"*N + "=1" + "\n"

import pwn
p = pwn.process("./envdb", env={"FLAG":"SSM{testflag}"})
p.send(payload0.encode())
p.send(payload1.encode())
print(p.recvall(timeout=1).decode())
