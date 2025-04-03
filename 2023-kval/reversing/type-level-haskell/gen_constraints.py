#!/usr/bin/env python3

import random
import string

flag = "typ35_4r3_0v3rp0w3red"

class Expr:
    def __init__(self, op, lhs = None, rhs = None):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __add__(self, other):
        return Expr("PAdd", self, other)

    def __mul__(self, other):
        return Expr("PMul", self, other)

    def __eq__(self, other):
        return Expr("PEq", self, other)

    def __repr__(self):
        l = "" if self.lhs is None else repr(self.lhs) + " "
        r = "" if self.rhs is None else repr(self.rhs) + " "
        return l + r + str(self.op)

def gen_succ(x):
    if (x == 0): return "Z"
    return f"(S {gen_succ(x-1)})"

def evaluate(expr, varnames, stack):
    if (expr.op == "x"):
        return "x"
    try:
        x = int(expr.op)
        return gen_succ(x)
    except:
        vn = varnames.pop(0)
        stack.append(expr.op + " " + evaluate(expr.lhs, varnames, stack) + " " + evaluate(expr.rhs, varnames, stack) + " " + vn)
        return vn

def brute_small_factor(x):
    for i in range(4,x):
        if x % i == 0:
            y = x // i
            if y < 10: return (i, y)
    return (-1, -1)

def gen_number(x):
    for i in range(x):
        y = x - i
        (a, b) = brute_small_factor(y)
        if (a != -1):
            a = gen_number(a)
            b = gen_number(b)
            if i == 0: return a * b
            else: return a * b + gen_number(i)
            break
    else:
        return Expr(x)

def gen_constraint(x, i):
    k = random.randrange(0, 25)
    n = random.randrange(1,25)
    kn = gen_number(k)
    nn = gen_number(n)
    xn = gen_number(n * x)
    xkn = gen_number(n * x + k)
    if (k == 0): ex = (nn * Expr("x") == xkn)
    else: ex = (nn * Expr("x") + kn == xkn)

    stack = []
    res = evaluate(ex, [x for x in string.ascii_lowercase], stack)
    random.shuffle(stack)
    #print(stack)
    constraints = ", ".join(stack)
    head = f"Apply C{i} x {res}"
    instance = f"instance ({constraints}) => {head}"
    return instance

alpha = "_" + string.ascii_lowercase + string.digits
flag = [alpha.index(x) for x in flag]

datas = [f"data C{i}" for i in range(len(flag))]
constraints = [gen_constraint(c, i) for (c, i) in zip(flag, range(len(flag)))]
checklist = " ::: ".join([f"C{i}" for i in range(len(flag))]) + " ::: E"
checklist = f"type Cs = {checklist}"

generated = datas + constraints + [checklist]
text = "\n".join(generated)

print(text)

with open("Main.hs", "r") as f:
    data = f.read()
    data = data.replace("--GENERATED-CONSTRAINTS--", text)
    print(data)
    with open("Constrained.hs", "w") as f2:
        f2.write(data)
