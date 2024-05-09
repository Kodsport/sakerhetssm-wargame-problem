import miniräknare
from Crypto.Util import number
import math

def modp(b, e, n):
    c = miniräknare.Calculator()

    for _ in range(e):
        c.press_buttons(f"{b}*")

    c.press_buttons(f"1%{n}")

    return c.press_button("=")

e = 3
m = number.bytes_to_long(b"SSM{********************}")

calc = miniräknare.Calculator()

calc.press_buttons(str(number.getPrime(1024)))
calc.press_button("*")
calc.press_buttons(str(number.getPrime(1024)))

n = calc.press_button("=")

print("e =", e)
print("n =", n)
print("c =", modp(m, e, n))
