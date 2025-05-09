from sage.all import *

e = 0x100

with open("modulus", "r") as f:
    n = int(f.readline())
    Z = Zmod(n)
    
with open("enc_flag", "r") as f:
    c = eval(f.readline())[0]
    c = matrix(Z, c)
    
with open("ai_weights", "r") as f:
    weights = eval(f.readline())
    weights = [matrix(Z, w) for w in weights]

with open("ai_biases", "r") as f:
    biases = eval(f.readline())
    biases = [matrix(Z, b) for b in biases]
  
weights_inverse = [W.inverse() for W in weights]

def backward_pass(x):
    for W, b in zip(weights_inverse[::-1], biases[::-1]):
        x = (x-b) * W   
    return x

for i in range(e):
    c = backward_pass(c)

flag = "".join([chr(a) for a in c[0]])
print(flag)