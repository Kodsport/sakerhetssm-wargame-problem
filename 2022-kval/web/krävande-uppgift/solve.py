import requests

from z3 import *

s = Solver()

# Lösenordet måste vara minst 15 tecken långt
# Lösenordet får inte vara mer än 15 tecken långt
length = 15
chars = [BitVec(f"char_{i}", 8) for i in range(length)]

# Endast följande tecknen är tillåtna i lösenordet: ABCDEFGHJLMOPQRSUVWXZabcdeghijklmnorsuvwyz1245689
allowed_chars = "ABCDEFGHJLMOPQRSUVWXZabcdeghijklmnorsuvwyz1245689"
for char in chars:
    s.add( Or([char == ord(c) for c in allowed_chars]))

# De sista tre tecknen i lösenordet måste vara siffror
for i in range(length-3, length):
    s.add( And(chars[i] >= ord("0"), chars[i] <= ord("9")) )

# Det första och andra tecknet i lösenord måste vara versaler
s.add( And(chars[0]>=ord("A"), chars[0]<=ord("Z")) )
s.add( And(chars[1]>=ord("A"), chars[1]<=ord("Z")) )

# Det femte tecknet i lösenordet måste vara ett Q
s.add( chars[4] == ord("Q") )

# Ordet "lol" måste finnas med i lösenordet
reqs = [And(chars[i]==ord("l"), chars[i+1]==ord("o"), chars[i+2]==ord("l")) for i in range(length-3)]
s.add(Or(reqs))

# Summan av ascii-värdena på de första tre tecknen måste vara 180
s.add(chars[0]+chars[1]+chars[2] == 180)

# Det åttonde och nionde tecknet i lösenordet måste vara samma
s.add(chars[7] == chars[8])

# De första åtta tecknen i lösenordet får inte vara sammma
s.add(Distinct(chars[0:8]))

# Summan av ascii-värdena på tecken nummer 6, 7, 8 och 9 måste vara 280
s.add(chars[5]+chars[6]+chars[7]+chars[8] == 280)

# Lösenordet måste sluta på ett tresiffrigt tal som är större än 800
s.add( Or(chars[length-3]==ord("8"), chars[length-3]==ord("9")) )

# Summan av ascii-värdena på alla tecken i lösenordet måste vara 1072
s.add( sum(chars) == 1072 )

def check_password(password):
    url = "http://127.0.0.1:50000/login"
    obj = {"username": "admin", "password": password}
    x = requests.post(url, data=obj)
    if "Ogiltigt lösenord" not in x.text:
        return True
    return False

# Hitta lösning
while s.check():
    model = s.model()

    # chr(int(str smh
    answer = "".join( chr(int(str(model[chars[i]]))) for i in range(length) )
    print(answer)

    if check_password(answer):
        print(answer)
        break

    s.add( Or( [chars[i] != model[chars[i]] for i in range(length)] ) )

