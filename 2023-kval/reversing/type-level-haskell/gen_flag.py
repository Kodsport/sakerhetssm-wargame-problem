#!/usr/bin/env python3
import string
import re

Z = "Z"
S = "S"
E = "E"

alpha = "_" + string.ascii_lowercase + string.digits
def gen_num(x):
    if (x == 0): return Z
    return f"({S} {gen_num(x-1)})"

flag = input("Enter the flag: ")
flag = re.match("SSM\{([a-z0-9_]+)\}", flag).group(1)
flag = [gen_num(alpha.index(x)) for x in flag]
flag = " ::: ".join(flag) + f" ::: {E}"

print("Paste the following type definition at the bottom of the haskell program:")
print("")
print(f"type Flag = {flag}")
print("")
print("Then run it with 'runghc challenge.hs'")
