#!/usr/bin/env python3

import base64
import random
import sys
import zlib

flag = sys.argv[1]

layer_tpl = """
global dig
def dig(code):
    thing = '%s'
    if len(code) == 0:
        print('Great job!')
        return
    
    if code[0] == '%s':
        thing = __import__("zlib").decompress(__import__("base64").b64decode(thing))
        thing = bytes(x^%#x for x in thing)
        thing = thing.decode()
        exec(thing)
        dig(code[1:])

    else:
        print('Nope!')
""".strip()


def generate_layer(letter: str, key: int, prev: str):
    prev = bytes(x^key for x in prev.encode())
    prev = zlib.compress(prev)
    prev = base64.b64encode(prev).decode()
    layer = layer_tpl % (prev, letter, key)
    return layer


prev = ''
for c in flag[::-1]:
    prev = generate_layer(c, random.randint(1, 256), prev)
    print(prev)

with open('challenge.py', 'w') as fout:
    fout.write('#!/usr/bin/env python3\n')
    fout.write(prev)
    fout.write('\n')
    fout.write('code = input("Which way do you want to go? ")\n')
    fout.write('assert len(code) == %d\n' % len(flag))
    fout.write('dig(code)\n')
