import random
from secrets import FLAG
import json

while True:
    p = random_prime(2^128)
    if p % 4 == 1:
        break

F = GF(p)

class LinearLayer:
    def __init__(self, dim, init_range=p):
        self.weights = [
            [random.randint(-init_range, init_range) for _ in range(dim)    ]
            for _ in range(dim)
        ]
        self.weights = Matrix(F, self.weights)

    def __call__(self, x):
        return self.weights * x
    
class Activation:
    def __init__(self, e = (p+1)//2):
        self.e = e

    def __call__(self, x):
        return vector(F, [x[i]^self.e for i in range(len(x))])

class NeuralNetwork:
    def __init__(self, dim):
        self.layers = [
            LinearLayer(dim, init_range=1000),
            Activation(),
            LinearLayer(dim)
        ]

    def __call__(self, x):
        x = vector(F, x)
        for layer in self.layers:
            x = layer(x)
        return x
    
def main():
    dim = 50
    enc = NeuralNetwork(dim)

    assert len(FLAG) == dim
    print(f"{p = }")
    print("Here is the encrypted flag:")
    print(list(enc(list(FLAG))))

    for i in range(60):
        inp = input("What would you like to encrypt? ")
        inp = json.loads(inp)
        
        assert type(inp) == list
        assert len(inp) <= dim
        for x in inp:
            assert type(x) == int
        
        inp = inp[:dim]
        inp = [0]*(dim-len(inp)) + inp
        inp = vector(F, inp)
    
        print(list(enc(inp)))

main()