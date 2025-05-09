# lösning utan z3

# regler:
# 1 & 2. len = 15
# 2. sista 3 måste vara nummer
# 3. ABCDEFGHJLMOPQRSUVWXZabcdeghijklmnorsuvwyz1245689 alfabet
# 4. första 2 bokstäver måste vara stora
# 5. 5:te bokstaven måste vara Q
# 6. måste innehålla lol
# 7. sum([:3]) = 180
# 8. [7] == [8]
# 9. len(set([:8])) == 8
# 10. sum([6:10]) == 280
# 11. int([:-3]) > 800
# 12. sum([:]) == 1072

# från detta kan vi lista ut att:
# första tecknen måste vara "AB1" eller "BA1", då det är det enda som funkar med regel 4, 7 och 9
# "lol" måste förekomma precis innan de 3 sista numren då det innehåller icke unika tecken och måste respektera regel 8 och 9
# därför har vi 2 delar av lösenordet som kan ändra på sig: tecken 4,6,7,8 samt siffrorna på slutet.

import itertools
import requests

alphabet = b"ABCDEFGHJLMOPQRSUVWXZabcdeghijklmnorsuvwyz1245689"
num_alphabet = b"1245689"

valid_nums = []

for split_num in itertools.product(num_alphabet, repeat=3):
    num = bytes(split_num)

    if not int(num) > 800:
        continue

    valid_nums.append(num)

for prefix in [b"AB1", b"BA1"]:
    for chars in itertools.product(alphabet, repeat=4):
        p = bytearray(
            prefix
            + bytes([chars[0]])
            + b"Q"
            + bytes(chars[1:])
            + bytes([chars[3]])
            + b"lolXXX"
        )

        # regel 10 och 9
        if not sum(p[5:9]) == 280 or not len(set(p[:8])) == 8:
            continue

        for num in valid_nums:
            p2 = p
            p2[-3:] = num

            # regel 12
            if sum(p2) == 1072:
                print(p2.decode())
                r = requests.post(
                    "http://127.0.0.1:50000/login",
                    data={"username": "admin", "password": p2.decode()},
                )

                if "Ogiltigt" not in r.text:
                    print(r.text)
                    exit()
