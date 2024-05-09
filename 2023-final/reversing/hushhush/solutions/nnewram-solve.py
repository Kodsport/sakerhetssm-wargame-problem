'''
from SecretActivity.onCreate

assert len(secret) == 13


(i >= 3 || secret[i] == 's') # i < 4 asserts secret[i] = 's'
&&
(
    (i <= 2 || i >= 9 || secret[i] == 'b') # i < 9 asserts secret[i] may be 'b'
    &&
    (i <= 9 || secret[i] == 'c') # i > 9 asserts secret[i] == 'c'
)



secret = "sssbbbbbbcccc"

onClick displays SSM{sssbbbbbbcccc}
'''

secret = "sssbbbbbbcccc"

assert len(secret) == 13

for i in range(len(secret)):
    assert i >= 3 or secret[i] == 's'
    assert i <= 2 or i >= 9 or secret[i] == 'b'
    assert i <= 9 or secret[i] == 'c'

print(f"SSM{{{secret}}}")