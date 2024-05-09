import hashlib

ADMIN_HASH = 0xf61e_a4e5_c9c2
MOD = 0xffff_ffff_ffff + 1

def do_sha256(data):
    hasher = hashlib.sha256()
    hasher.update(data)
    return int.from_bytes(hasher.digest(), byteorder="little") % MOD

inv = {}
for i in range(10**8):
    if i % 100_000 == 0:
        print(f"{i = }")
    s = str(i)
    h = do_sha256(s.encode("utf8"))
    inv[h] = s
    h2 = (((ADMIN_HASH - h*0x123321)*pow(0x321123, -1, MOD)) % MOD + MOD) % MOD
    assert (h*0x123321 + h2*0x321123) % MOD == ADMIN_HASH
    if h2 in inv:
        print(f"username = {s}")
        print(f"password = {inv[h2]}")
        break
