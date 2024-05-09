import socket, sys
import ctypes

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))

DEBUG = False

def read_line():
    buf = b""
    while True:
        ch = s.recv(1)
        if ch == b'\n':
            if DEBUG:
                print("<", buf)
            return buf
        buf += ch

read_line() # intro

l = ctypes.CDLL("libc.so.6")

t = l.time(ctypes.c_void_p(0))

def pw_for(dt):
    l.srand(t + dt)

    pw = ctypes.c_uint64(1)
    for _ in range(5):
        pw = ctypes.c_uint64(pw.value * l.rand())

    return pw.value

for dt in range(0, 20):
    for dt_ in [dt, -dt]:
        s.send(str(pw_for(dt_)).encode() + b'\n')
        line = read_line()
        if b'Grattis' in line:
            print(line.decode())
            exit()
