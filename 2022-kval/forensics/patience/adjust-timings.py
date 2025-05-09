#!/usr/bin/env python3

import sys
import struct

MARKER_BYTES = bytes.fromhex('21 F9 04 01 13 37')

if len(sys.argv) < 4:
    print(f'Usage: {sys.argv[0]} input.gif output.gif <num_frames>')
    sys.exit(1)

num_frames = int(sys.argv[3])

with open(sys.argv[1], 'rb') as fin:
    image = bytearray(fin.read())

for _ in range(num_frames-3):
    offset = image.find(MARKER_BYTES)
    if offset == -1:
        print(f'ERROR: Could not find marker, exiting')
        sys.exit(1)
    image[offset+4:offset+6] = struct.pack('<H', 100)

for _ in range(3):
    offset = image.find(MARKER_BYTES)
    if offset == -1:
            print(f'ERROR: Could not find marker, exiting')
            sys.exit(1)
    image[offset+4:offset+6] = struct.pack('<H', 0xFFFF)

with open(sys.argv[2], 'wb') as fout:
    fout.write(image)
