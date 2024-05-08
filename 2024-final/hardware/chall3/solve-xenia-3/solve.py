import time
from tqdm import tqdm

# from https://gist.github.com/rgov/891712
def deBruijn(n, k):
    '''
    An implementation of the FKM algorithm for generating the de Bruijn
    sequence containing all k-ary strings of length n, as described in
    "Combinatorial Generation" by Frank Ruskey.
    '''

    a = [0] * (n + 1)

    def gen(t, p):
        if t > n:
            for v in a[1:p + 1]:
                yield v
        else:
            a[t] = a[t - p]

            for v in gen(t + 1, p):
                yield v

            for j in range(a[t - p] + 1, k):
                a[t] = j
                for v in gen(t + 1, t):
                    yield v

    return gen(1, 1)


from logicanalyzer import LogicAnalyzer, Port
anal = LogicAnalyzer()

print("""
Connect GND to GND.
Connect Port A 1-4 to digits 0-3
""")

# set pin A 1-4 to output
for i in range(1, 5):
    anal.set_gpio_mode(Port.A, i, output=True)

def send(digit):
    for i in range(1, 5):
        anal.set_gpio_level(Port.A, i, high = not (digit == i))
    time.sleep(0.01)
    for i in range(1, 5):
        anal.set_gpio_level(Port.A, i, high = True)

for x in tqdm(list(deBruijn(4, 7))):
    send(x)
