from pwn import *
import z3

def sep(data, sl):
    return [data[i:i+sl] for i in range(0, len(data), sl)]

def get_flag():
    if len(sys.argv) > 1:
        r = remote(sys.argv[1], int(sys.argv[2]))
    else:
        r = process("../docker/files/nonlinear")
    
    s = z3.Solver()

    sgp = z3.BitVec("seed_glob_ptr", 64) # &seed

    def next_rand(seed):
        return seed * seed + sgp

    r.recvuntil("Encrypted data: ")
    flag_parts = [int(part, 16) for part in sep(r.recvline().decode().strip(), 8 * 2)]

    constdata = 0x4141414141414141

    all_vecs = [z3.BitVec(f"flag_key_{i}", 64) for i in range(8)]

    r.sendline(b"A" * 64)
    r.recvuntil("Encrypted data: ")
    
    parts = sep(r.recvline().decode().strip(), 8 * 2)
    print(parts)
    vecs = [z3.BitVec(f"data_{ei}_{i}", 64) for i in range(len(parts))]

    all_vecs += vecs

    for vec, val in zip(vecs, parts):
        print(vec, val, hex(int(val, 16) ^ constdata))
        s.add(vec == int(val, 16) ^ constdata)

    s.add(all_vecs[0] == next_rand(0xdeadbeefcafebabe))
        
    for a, b in zip(all_vecs, all_vecs[1:]):
        print(a, b)
        s.add(next_rand(a) == b)

    while s.check() == z3.sat:
        m = s.model()

        flag = b""
        for fp, fk in zip(flag_parts, all_vecs):
            flag += (fp ^ m[fk].as_long()).to_bytes(8, "little")
            print(flag)
        
        s.add(sgp != m[sgp])
        yield flag
    
    r.close()

with open("../docker/files/flag.txt", "rb") as ff:
    flag = ff.read()
    flaggen = get_flag()
    for attempt in range(100):
        if any(b"SSM" in possible_flag for possible_flag in get_flag()):
            print(f"Found flag: {flag}")
            exit(0)

    print("Could not find the flag.")
    exit(1)

 