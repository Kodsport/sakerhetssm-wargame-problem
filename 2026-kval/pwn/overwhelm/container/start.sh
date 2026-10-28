#!/usr/bin/env bash
set -euo pipefail

exec socat \
  TCP-LISTEN:1337,reuseaddr,fork \
  EXEC:"/home/ctf/chall",pty,stderr
