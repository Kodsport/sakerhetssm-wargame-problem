import sys
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))

def bytes_to_binary(b):
    return [(x >> i) & 1 for x in b for i in range(8)]

def binary_to_bytes(b):
    o = bytes()
    for i in range(0, len(b), 8):
        n = 0
        for j in range(8):
            n |= b[i+j] << j
        o = o + bytes([n])
    return o

def similarity(plaintext, solution):
    assert(len(plaintext) == len(solution))
    diffs = [x == y for x, y in zip(bytes_to_binary(plaintext), bytes_to_binary(solution))]
    return sum(diffs) / len(diffs)

def last_block_similarity(res, all_sim, known):
    n_blocks = len(res) // 16
    return (all_sim * n_blocks - similarity(res[:-16], known) * (n_blocks - 1))

def recvnl():
    buf = b''
    while True:
        c = s.recv(1)
        if c == b'\n':
            break
        buf = buf + c
    # print("> ", buf, file=sys.stderr)
    return buf

def get_for(data, known):
    intro = recvnl()
    s.send(data.hex().encode() + b"\n")
    # time.sleep(0.01)
    line1 = recvnl()
    line2 = recvnl()

    decrypted = bytes.fromhex(line1[len("Your decrypted data is "):].decode())
    sim = float(line2[len("Your data is "):line2.index(b"%")].decode()) / 100
    return decrypted, last_block_similarity(decrypted, sim, known)

known = b"Here's your flag: "[:16]

prefix = b''
altering = b'\x00' * 16
suffix = b'\x00' * 16

while True:
    _, score = get_for(prefix + altering + suffix, known)

    for bit in range(16 * 8):
        altered = bytes_to_binary(altering)
        altered[bit] ^= 1
        altered = binary_to_bytes(altered)

        out, v = get_for(prefix + altered + suffix, known)

        print(out.hex(), v, out[len(prefix)+len(altered):], file=sys.stderr)
        if v > score:
            score = v
            altering = altered
        if v == 1:
            decoded = out[-16:]
            print("SUCCESS:", decoded, file=sys.stderr)
            known = known + decoded
            break

    if score != 1:
        print("Done. Decrypted data:", file=sys.stderr)
        print(known.decode())
        break

    prefix = prefix + altering
    altering = b'\x00' * 16
