#!/usr/bin/env python3

from time import sleep

def compare_password(p1, p2):

    # NOT LEAKING PASSWORD LENGTH!!
    if len(p1) < len(p2):
        p1 = p1.ljust(len(p2), "0")
    else:
        p2 = p2.ljust(len(p1), "0")

    # compare passwords
    for i, c in enumerate(p1):
        if not c == p2[i]:
            return False

        # Delay added for professional security
        sleep(.08)

    return True

if __name__ == "__main__":
    from FLAG import FLAG
    print("Input password:")
    password = input()
    while not compare_password(password, FLAG):
        print("Incorrect password! No cat for you!")
        print("Input password:")
        password = input()
    print("Unlocked! Here is a cat picture:", flush=True)
    sleep(2)
    with open("public_domain_cat.jpg", "rb") as file:
        print(file.read())
