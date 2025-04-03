#!/bin/bash

# Kompileringen behöver använda python 3.8, förslagsvis i Docker

docker run -it -v $PWD:/chall.src python:3.8.16-alpine3.17 python3 -m compileall chall.src/chall.py

cp __pycache__/chall* chall.pyc

rm chall.zip

zip chall.zip __main__.py chall.pyc

echo '#!/usr/bin/env python3' > chall

cat chall.zip >> chall

chmod +x chall

# För att testa:

# docker run -it -v $(pwd):/chall.src python:3.8.16-alpine3.17 /bin/sh
