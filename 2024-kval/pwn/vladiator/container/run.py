#!/usr/bin/python3

from time import sleep

import tempfile
import shutil
import base64
import stat
import os

print("I'll deploy whatever binary you give me")
print("... Just make sure that it's signed, ok?")
sleep(2)

print("I'll give you a signed binary to start of with.")
sleep(1)

with open("/lib/x86_64-linux-gnu/libc.so.6", "rb") as f:
    print("libc:", base64.b64encode(f.read()).decode())

line = input("File (base64): ")

with tempfile.NamedTemporaryFile() as f:

    f.write(base64.b64decode(line))

    os.chmod(f.name, os.stat(f.name).st_mode | stat.S_IEXEC)
    shutil.copy(f.name, f.name + ".elf")

os.system("/home/ctf/ELFSign -c -p /home/ctf/pubkey.pem -e " + f.name + ".elf")

os.remove(f.name + ".elf")