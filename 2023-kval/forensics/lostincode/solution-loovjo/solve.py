from tempfile import TemporaryDirectory

import os
from zipfile import ZipFile
import bz2
import gzip
import base64
import binascii
import shutil


with TemporaryDirectory() as d:
    print("boop", d)
    shutil.copyfile("../flag", os.path.join(d, "flag-0"))

    i = -1
    while True:
        i += 1

        fname = os.path.join(d, f"flag-{i}")
        dname = os.path.join(d, f"flag-{i+1}")

        with open(fname, "br") as f:
            hdr = f.read(2)
            f.seek(0, 3)
            sz = f.tell()
            if hdr == b'PK':
                ty = "zip"
            elif hdr == b'\x1f\x8b':
                ty = "gz"
            elif hdr == b'BZ':
                ty = "bz2"
            else:
                ty = "b64"

        print(f"Iteration {i}: {ty} ({sz/1000:.2f}kB)")

        if ty == 'zip':
            with ZipFile(fname, "r") as zf:
                unzip = zf.read("flag")
            with open(dname, "wb") as dest:
                dest.write(unzip)

        elif ty == 'gz':
            with gzip.open(fname, "rb") as gzf:
                ungzip = gzf.read()
            with open(dname, "wb") as dest:
                dest.write(ungzip)

        elif ty == 'bz2':
            with bz2.open(fname, "rb") as bzf:
                unbzip = bzf.read()
            with open(dname, "wb") as dest:
                dest.write(unbzip)

        elif ty == 'b64':
            with open(fname, "br") as f:
                data = f.read()
                try:
                    unb64 = base64.b64decode(data)
                except binascii.Error:
                    print("base 64 broke")
                    print(data)
                    # XOR the flag with WestWest...
                    exit(0)
            with open(dname, "wb") as dest:
                dest.write(unb64)
