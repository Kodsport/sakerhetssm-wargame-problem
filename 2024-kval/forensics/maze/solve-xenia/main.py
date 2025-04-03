import struct
from sys import stderr
def eprint(*x):
    print(*x, file=stderr)

# Each entry seems to be at 0x14000 + 0x200 * (N-1)
# Each entry has a number of entries, each having a name (11 chars + nl + 4 null bytes)
# After that, 8 null bytes, after that the N of the directory

def parse_entry(f, N):
    f.seek(0x14200 + 0x200 * (N - 2))
    d = f.read(0x200)
    entries = struct.unpack(
        "11sxxxxxxxxxxxxxxxHxxxx"*16,
        d,
    )
    entries = zip(entries[::2], entries[1::2])

    return [(e[0].rstrip(), e[1]) for e in entries if e[0] != b'\x00' * 11]

with open("../filesystem", "rb") as f:
    seen = set()
    visiting = [(2, b"S", [])] # [(index, name, [path])], path being (idx, name)

    while len(visiting):
        idx, name, path = visiting.pop(0)
        if name in {b'.', b'..'}:
            continue

        if idx in seen:
            continue
        if idx in [i for i, n in path]:
            continue

        seen.add(idx)

        try:
            name = name.decode()
        except UnicodeDecodeError as e:
            eprint("Error at block", hex(idx), "= offset", hex(0x14200 + 0x200 * (idx - 2)))
            continue

        spath = path + [(idx, name)]

        for subname, sidx in parse_entry(f, idx):
            if subname.startswith(b"flag") and subname.endswith(b"txt"):
                flag = "".join([name for idx, name in spath])
                flag_slash = "/".join([name for idx, name in spath])
                eprint("Found flag.txt")
                print(flag)
                eprint(f"In folder {flag_slash}/{subname.decode()}")
                eprint(f"Flag entry {hex(sidx)}, offset {hex(0x14200 + 0x200 * (sidx-2))}")
                for i in range(3):
                    pidx, pname = spath[len(spath) - i - 1]
                    eprint(f"Parent #{i} {pname!r} entry {hex(pidx)}, offset {hex(0x14200 + 0x200 * (pidx-2))}")

            visiting.append((sidx, subname, spath))
