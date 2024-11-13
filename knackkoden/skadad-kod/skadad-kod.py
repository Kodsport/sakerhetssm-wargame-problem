from time import sleep
import subprocess
import psutil
import base64
import os
def dump_program(pid):
    with open(f"/proc/{pid}/mem", "rb") as memf, open(f"/proc/{pid}/maps", "rb") as mapf:
        maps = []
        for line in mapf.readlines():
            if b'r' not in line.split()[1]: break
            start, end = line.split()[0].split(b"-")
            start, end = int(start, 16), int(end, 16)
            name = line.split()[-1]
            try:
                memf.seek(start)
                b = memf.read(end - start).hex()
            except:
                pass
            maps.append((name.decode(), start, end, b))
    back = base64.b64encode(repr(maps).encode()).decode()
    print(f"The b64 dump will be of size: {len(back)}")
    print(back)
dump_program(int(input("pid: ")))