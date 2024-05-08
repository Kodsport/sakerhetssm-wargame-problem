#!/usr/bin/env python3

import zipfile
import itertools
import io

parts = []
for i in range(1,5+1):
    with open(f'part{i}', 'rb') as fin:
        parts.append(fin.read())

for cand_parts in itertools.permutations(parts):
    cand_zip = b''.join(cand_parts)
    zipdata = io.BytesIO(cand_zip)

    try:
        archive = zipfile.ZipFile(zipdata)
        flagdata = archive.read('image_flag.jpg')
        with open('flag.jpg', 'wb') as fout:
            fout.write(flagdata)
        print('Found flag!')
        break
    except:
        continue
