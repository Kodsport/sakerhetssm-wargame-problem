import hashlib
from tqdm import tqdm

WANTED = 0xf61ea4e5c9c2

def do_sha256(data):
    hasher = hashlib.sha256()
    hasher.update(data)
    return int.from_bytes(hasher.digest(), byteorder="little")

def hash_login(username, password):
    return (do_sha256(username) * 0x123321 + do_sha256(password) * 0x321123) & 0xffff_ffff_ffff

def make_bytes(num):
    return str(num).encode()


passwords = {}
for i in tqdm(range(2**24)):
    pw = make_bytes(i)
    passwords[(do_sha256(pw) * 0x321123) & 0xffff_ffff_ffff] = pw

for i in tqdm(range(2**24 * 10)): # 2**24 only has about 63% chance working. * 10 to be v safe
    un = make_bytes(i)
    un_hash = do_sha256(un) * 0x123321

    wanted_pw_hash = (WANTED - un_hash) & 0xffff_ffff_ffff

    if wanted_pw_hash in passwords:
        pw = passwords[wanted_pw_hash]
        print(un, pw)
        break
