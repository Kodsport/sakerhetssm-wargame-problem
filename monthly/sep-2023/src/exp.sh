#!/bin/sh
clang -O2 -target bpf -o bpf_filter -c filter.c && llvm-objdump-14 -d bpf_filter | python3 dumptobarr.py
