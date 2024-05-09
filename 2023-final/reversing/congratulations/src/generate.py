#!/usr/bin/env python3

import base64
import sys
import re

inpath = sys.argv[1]
outpath = sys.argv[2]

with open(inpath, 'r') as fin:
    indata = fin.read()

code_pattern = r'\/\*<obfuscate>\*\/(.*)\/\*<\/obfuscate>\*\/'
code_match = re.search(code_pattern, indata, flags=re.MULTILINE|re.DOTALL)

to_obfuscate = code_match[1]
obfuscated = []
key = 0x13
for c in to_obfuscate.encode():
    obfuscated.append(c ^ key)
    key = (key + 1) & 0xFF
obfuscated_b64 = base64.b64encode(bytes(obfuscated)).decode()
obfuscated_code = f'let validate = "{obfuscated_b64}";'

updated_code = re.sub(code_pattern, obfuscated_code, indata, flags=re.MULTILINE|re.DOTALL)
updated_code = updated_code.replace('/*<decrypt>*/', '')
updated_code = updated_code.replace('/*</decrypt>*/', '')
updated_code = updated_code.replace('//<call:decrypt>', 'eval(decrypt(validate));')

with open(outpath, 'w') as fout:
    fout.write(updated_code)
