import hashlib
import sys

import numpy as np
import random

CHUNK_SIZE = 16

ADMIN_HASH = bytes.fromhex("6f520d05881ee30555aea7d0878ef923aa4e29e2235303cb032174e95f8bbe3f")

def sha256(data):
    h = hashlib.sha256()
    h.update(data)
    return h.digest()

def hash_block(blk):
    h1 = sha256(bytes(blk, "ascii"))
    h2 = sha256(h1)
    return h2

def get_bits(b):
    return [(x >> i) & 1 for x in b for i in range(7, -1, -1)]

def gf2mult(a, b):
    return (a @ b) % 2

def gf2add(a, b):
    return a ^ b

# finds an x such that A @ x = b
# gaussian elimination
def solve(A, b):
    M = np.hstack((A, b[:, np.newaxis]))

    for col in range(256):
        pivot_row = -1
        for row in range(col, 256):
            if M[row, col] == 1:
                pivot_row = row
                break

        if pivot_row == -1:
            raise ValueError(f"Singular matrix 3: (got to col {col})")

        row_content = np.copy(M[pivot_row])
        M[pivot_row] = M[col]
        M[col] = row_content

        for row in range(256):
            if row == col:
                continue

            if M[row, col] == 1:
                M[row, :] ^= row_content

    return M[:, 256]

for attempt in range(100):
    blocks = []
    A = np.zeros((256, 0), "u8")
    for i in range(256):
        block_content = f"meow{attempt}-{i}".ljust(CHUNK_SIZE, "x")
        hashed = hash_block(block_content)
        hashed_bits = get_bits(hashed)

        blocks.append(block_content)

        A = np.hstack((A, np.array(hashed_bits, "u8")[:, np.newaxis]))

    wanted = np.array(get_bits(ADMIN_HASH), "u8")

    try:
        x = solve(A, wanted)

    except ValueError as e:
        print(f"Attempt {attempt} failed: {e}", file=sys.stderr)
        continue

    data = ""
    for should_use, block in zip(x, blocks):
        if should_use:
            data += block

    print(data)

    break
