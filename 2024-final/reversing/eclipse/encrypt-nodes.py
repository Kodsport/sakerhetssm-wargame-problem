#!/usr/bin/env python3

import struct
import sys
import lief

input_path = sys.argv[1]
output_path = sys.argv[2]

with open(input_path, 'rb') as fin:
    input_data = bytearray(fin.read())

input_elf = lief.parse(input_path)
for s in input_elf.symbols:
    if s.type != lief.ELF.SYMBOL_TYPES.FUNC:
        continue
    if not s.name.startswith('node'):
        continue
    if s.name.endswith('_pre'):
        continue
    
    node_key = input_elf.get_symbol(f'{s.name}_key')
    node_key_offset = input_elf.virtual_address_to_offset(node_key.value)
    node_len = input_elf.get_symbol(f'{s.name}_len')
    node_len_offset = input_elf.virtual_address_to_offset(node_len.value)
    node_offset = input_elf.virtual_address_to_offset(s.value)

    enc_key = input_data[node_key_offset:node_key_offset+node_key.size]
    #print(f'Encrypting {s.name} (len: {s.size}), key: {enc_key.hex()}')

    # Encrypt function
    node_data = input_data[node_offset:node_offset+s.size]
    #print(f'Plaintext: {node_data.hex()}')
    node_enc_data = bytes(x^enc_key[i%node_key.size] for i,x in enumerate(node_data))
    input_data[node_offset:node_offset+s.size] = node_enc_data

    # Store length
    input_data[node_len_offset:node_len_offset+node_len.size] = struct.pack('<Q', s.size)

with open(output_path, 'wb') as fout:
    fout.write(input_data)
