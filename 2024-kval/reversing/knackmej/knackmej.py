#!/usr/bin/env python3

def add(a, k):
    return bytes([(c + k) % 256 for c in a])

def xor(a, k):
    return bytes([c ^ k for c in a])

flag = b"SSM{Julen_ar_har_sa_at_lite_knack}"

t = add(flag, 30).hex().encode()
print(t)
target = xor(t, 42)

print("\\x" + "\\x".join(["%02x" % b for b in target]))
print(len(target))
