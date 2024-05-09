import pwn, struct
import sys

s = pwn.remote(sys.argv[1], int(sys.argv[2]), ssl=True)

print(s.recv(10000))
s.send(b"8\n")
print(s.recv(10000))

# Vi vill söka bit för bit. Vi utgår från bara 1:or, då är det lägre risk att vi slår i ett skumt tecken som scanf blir ledsen av (\n, \t, etc.)

buf = b'\xff' * 60

for byte in range(len(buf)):
    for bit in range(8):
        bitted = buf[:byte] + bytes([buf[byte] & ~(128 >> bit)]) + buf[byte+1:]
        print(">", bitted)

        s.send(bitted + b"\n")
        res = s.recv(1000)
        print("<", res)
        print()

        if res.startswith(b"Du vann"):
            print(buf)
            exit()

        if res.startswith("För stort".encode()):
            buf = bitted

        if not res.endswith(b"Du gissar: "):
            s.recv(1000)

