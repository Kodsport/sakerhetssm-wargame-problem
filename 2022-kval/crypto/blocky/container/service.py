#!/usr/bin/env python3
from Crypto.Cipher import AES
import secrets, base64
from flag import flag

key = secrets.token_bytes(16)

def register():
    print("--REGISTER--")
    print("Give username:")
    username = input("> ")
    username = username.replace("&", "").replace("=", "")
    profile = "admin=false&username=" + username
    iv = secrets.token_bytes(16)
    aes = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    encrypted = aes.encrypt(profile.encode())
    profile = base64.b64encode(iv + encrypted)
    print("Here is your profile:", profile.decode())

def parse_profile(profile):
    profile = profile.strip().split(b"&")
    data = {}
    for kv in profile:
        k, v = kv.split(b"=")
        data[k] = v
    return data

def is_admin(profile):
    return profile[b"admin"] == b"true"

def login():
    print("--LOGIN--")
    print("Provide profile:")
    try:
        enc_profile = base64.b64decode(input("> "))
        aes = AES.new(key, AES.MODE_CFB, iv=enc_profile[:16], segment_size=128)
        profile = aes.decrypt(enc_profile[16:])
        profile = parse_profile(profile)
        if is_admin(profile):
            print("Welcome admin!")
            print(flag)
        else:
            print("Welcome:", profile[b"username"].decode())
    except:
        print("Bad login!")

def banner():
    print(" ######                                    ")
    print(" #     # #       ####   ####  #    # #   # ")
    print(" #     # #      #    # #    # #   #   # #  ")
    print(" ######  #      #    # #      ####     #   ")
    print(" #     # #      #    # #      #  #     #   ")
    print(" #     # #      #    # #    # #   #    #   ")
    print(" ######  ######  ####   ####  #    #   #   ")

def main():
    banner()
    while True:
        print("------------ Blocky -----")
        print("- The best social media!")
        print("1. Register")
        print("2. Log in")
        print("3. Exit")

        try:
            choice = int(input("> "))
            assert choice in [1, 2, 3]
        except:
            print("Bad choice!")
            continue
        if choice == 1:
            register()
        elif choice == 2:
            login()
        elif choice == 3:
            return

if __name__ == "__main__":
    main()
