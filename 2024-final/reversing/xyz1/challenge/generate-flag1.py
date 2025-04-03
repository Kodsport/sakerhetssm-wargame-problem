#!/usr/bin/env python3

import sys

flag = sys.argv[1]

template_c = """
#include "flag.h"

const unsigned char flagenc[] = {{
    {flagenc}
}};
const size_t flaglen = {flaglen};
"""

template_h = """
#include <stddef.h>

extern const unsigned char flagenc[];
extern const size_t flaglen;
"""

flagenc = bytes(x ^ i ^ 0x42 for i, x in enumerate(flag.encode()))
flagenc_fmt = ', '.join(f'{x:#02x}' for x in flagenc)

with open('flag.c', 'w') as fout:
    fout.write(
        template_c.format(**{
            'flagenc': flagenc_fmt,
            'flaglen': len(flagenc)
        }))
with open('flag.h', 'w') as fout:
    fout.write(template_h)
