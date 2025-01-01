import string

word = "2020pds{nwn_vådr_ck_nååäbyeåqn_zrå_v_nyyn_snyy_yvdr}"
upper_letters = string.ascii_uppercase + "ÅÄÖ"
lower_letters = string.ascii_lowercase + "åäö"

output = ""
for c in word:
    if c in upper_letters:
        idx = (upper_letters.index(c)-13) % len(upper_letters)
        output += upper_letters[idx]
    elif c in lower_letters:
        idx = (lower_letters.index(c)-13) % len(lower_letters)
        output += lower_letters[idx]
    else:
        output += c

print(output)
