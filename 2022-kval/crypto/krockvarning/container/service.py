#!/usr/bin/env python3
from Crypto.Cipher import AES
import secrets, random, sys
from flag import flag

def hash_string(message):
    """ Compute the hash of message.
    if message = B1;B2;B3;...Bn and Bi are blocks of 128 bits
    computers DEC(....DEC(DEC(B1, B2), B3)...), Bn)
    where DEC is AES decryption
    """
    block = message[:16]
    # pad first block
    block = block + (b" " * (16-len(block)))
    for i in range(16, max(32, len(message)), 16):
        # extract the i-th block
        key = message[i:i+16]
        # pad the i-th block
        key = key + (b" " * (16-len(key)))
        cipher = AES.new(key, AES.MODE_ECB)
        block = cipher.decrypt(block)
    return block

def banner():
    print('              ____----------- _____')
    print('\~~~~~~~~~~/~_--~~~------~~~~~     \\')
    print(' `---`\  _-~      |                   \\')
    print('   _-~  <_         |                     \[]')
    print(" / ___     ~~--[""] |      ________-------'_")
    print('> /~` \    |-.   `\~~.~~~~~                _ ~ - _')
    print(' ~|  ||\%  |       |    ~  ._                ~ _   ~ ._')
    print('   `_//|_%  \      |          ~  .              ~-_   /\\')
    print('          `--__     |    _-____  /\               ~-_ \/.')
    print('               ~--_ /  ,/ -~-_ \ \/          _______---~/')
    print('                   ~~-/._<   \ \`~~~~~~~~~~~~~     ##--~/')
    print('                         \    ) |`------##---~~~~-~  ) )')
    print('                          ~-_/_/                  ~~ ~~')

def main():
    banner()
    print("------------ Krockvarning -----")
    for _ in range(100):
        chall = secrets.token_bytes(random.randint(33, 47))
        print("Find collision:", chall.hex())
        try:
            collision = bytes.fromhex(input("> "))
        except:
            print("Bad input!")
            sys.exit(0)
        if chall == collision or hash_string(chall) != hash_string(collision):
            print("No collision!")
            sys.exit(0)
    print(flag)

if __name__ == "__main__":
    main()
