import subprocess
import sys

proc = subprocess.Popen("container/service.py", stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def read_until(text):
    assert isinstance(text, bytes)
    buf = b""
    while True:
        if buf[-len(text):] == text:
            return buf
        buf += proc.stdout.read(1)

for i in range(100):
    read_until(b"Find collision: ")
    a = read_until(b"\n")[:-1]
    proc.stdin.write(a)
    proc.stdin.write(b'20\n')
    proc.stdin.flush()

sys.stdout.buffer.write(proc.stdout.read())
