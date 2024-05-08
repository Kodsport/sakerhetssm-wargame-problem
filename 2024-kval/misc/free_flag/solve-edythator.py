from hashlib import md5
from string import printable

hashes = {md5(x.encode()).hexdigest(): x for x in printable}
file = open('chall.txt', 'r').readlines()

[print(hashes[x[:-1]], end='') for x in file]
print()