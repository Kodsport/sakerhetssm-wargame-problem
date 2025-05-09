#!/bin/sh

set -e

python3 patch.py
chmod +x /tmp/patched
/tmp/patched
