#!/usr/bin/python3
import tempfile
import sys
import os

nchars = int(input("Input length: "))
data = sys.stdin.buffer.read(nchars)

with tempfile.NamedTemporaryFile() as fp:
    fp.write(data)
    fp.flush()
    os.system(f"./stdmap < {fp.name}")
