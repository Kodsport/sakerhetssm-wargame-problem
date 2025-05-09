#!/usr/bin/env python3
import string
import itertools
import random

with open("Constrained.hs", "r") as f:
    data = f.read()

no_reorder = ["Flag", "Reify", "ToString"]
def order(line):
    if "{-#" in line: return 0
    if all([x not in line for x in no_reorder]):
        if "data" in line: return 100 #+ random.randrange(99)
        if "type" in line: return 200 + random.randrange(99)
        if "class" in line: return 300 + random.randrange(99)
        if "instance" in line: return 400 + random.randrange(99)
    return 500

up = "MNO"
symbols = list(up) + [a + b for (a,b) in itertools.product(up, up)]
#for banned in ["S", "Z", "T", "F", "E"]: symbols.remove(banned)

def get_symbol():
    global symbols
    return symbols.pop(0)

def isupper(x): return x in string.ascii_uppercase

#renames = ["data", "class", "type"]
renames = ["class", "type", "data"]
rename_syms = ["PAdd", "PMul", "PEq"]

def is_valid_rename(line):
    return any([x in line for x in renames]) \
        and isupper(line.split()[1][0]) \
        and any([line.split()[1] == x for x in rename_syms])

def renameline(line, names, syms):
    for (a,b) in zip(names, syms):
        line = line.replace(a,b)
        line = line.replace(a,b)
    return line

def rename(line, d):
    if not is_valid_rename(line): return d
    name = " " + line.split()[1] + " "
    name2 = "(" + name[1:]
    name3 = name[:-1] + "\n"
    name4 = name[:-1] + ")"

    sym = " " + get_symbol() + " "
    sym2 = "(" + sym[1:]
    sym3 = sym[:-1] + "\n"
    sym4 = sym[:-1] + ")"
    print("Replace" + name +"with" + sym)
    return [renameline(x, [name,name2,name3,name4], [sym,sym2,sym3,sym4]) for x in d]

def rename_all(data):
    new_data = [x for x in data]
    for line in data:
        new_data = rename(line, new_data)
    return new_data

data = data.split("\n")
data = [x for x in data if "--" not in x or "---" in x]
data = [(order(x), x) for x in data]
#data = sorted(data, key = lambda x: x[0])
data = [x[1] + "\n" for x in data]
#data = rename_all(data)
data = [x[:-1] for x in data]

with open("challenge.hs", "w") as f:
    f.write("\n".join(data))
