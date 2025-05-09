#!/bin/env python3
import random
import shutil
import os
import stat

random.seed(13333337)

order = list(range(1, 256))
random.shuffle(order)
order = [0] + order + [256]
filenames = list(range(1, 256))
random.shuffle(filenames)
filenames = [0] + filenames

for i in range(256):
    shutil.copy("exec", f"exec{filenames[i]}")
    os.chown(f"exec{filenames[i]}", order[i + i % 2], order[i + (i + 1) % 2])
    os.chmod(
        f"exec{filenames[i]}",
        stat.S_IROTH
        | stat.S_IRGRP
        | stat.S_IRUSR
        | stat.S_IXGRP
        | stat.S_IXUSR
        | stat.S_ISUID
        | stat.S_ISGID,
    )
