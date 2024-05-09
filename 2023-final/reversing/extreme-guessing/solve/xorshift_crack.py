import numpy as np
import struct

def to_double(st0):
    n = 0x3FF0000000000000 | (st0 >> 12)
    return struct.unpack("d", struct.pack("Q", n))[0] - 1

PLOT = False

if PLOT:
    import matplotlib.pyplot as plt

UINT64 = (1<<64)-1

def xorshift128_n(state0, state1):
    # uint64_t s1 = *state0;
    # uint64_t s0 = *state1;
    # *state0 = s0;
    # s1 ^= s1 << 23;
    # s1 ^= s1 >> 17;
    # s1 ^= s0;
    # s1 ^= s0 >> 26;
    # *state1 = s1;
    s1 = state0
    s0 = state1

    s1 ^= (s1 << 23) & UINT64
    s1 ^= (s1 >> 17)
    s1 ^= s0 & UINT64
    s1 ^= (s0 >> 26) & UINT64

    return s0, s1

# from my solve script of SHA (kval)
# finds an x such that A @ x = b
# gaussian elimination
def solve(A, b):
    M = np.hstack((A, b[:, np.newaxis]))

    for col in range(128):
        pivot_row = -1
        for row in range(col, 128):
            if M[row, col] == 1:
                pivot_row = row
                break

        if pivot_row == -1:
            raise ValueError(f"Singular matrix 3: (got to col {col})")

        row_content = np.copy(M[pivot_row])
        M[pivot_row] = M[col]
        M[col] = row_content

        for row in range(128):
            if row == col:
                continue

            if M[row, col] == 1:
                M[row, :] ^= row_content

    return M[:, 128]


# xorshift is a fully linear operation in GF(2)
# we will represent it as a linear transformation using a 128x128 matrix

def state_vec(state0, state1):
    state0_v = (state0 >> np.arange(64)) & 1
    state1_v = (state1 >> np.arange(64)) & 1
    return np.hstack((state0_v, state1_v))

def vec_state(state_v):
    state0_v, state1_v = state_v[:64], state_v[64:]

    space = np.logspace(0, 63, 64, base=2, dtype="uint64")
    state0 = (state0_v * space).sum()
    state1 = (state1_v * space).sum()
    return state0, state1

assert vec_state(state_vec(123, 321)) == (123, 321)

# helper function for generating xor calls
# state[dest_start:dest_start+n_bits] ^= state[source_start:source_start+n_bits]
def xor_op(dest_start, source_start, n_bits):
    res = np.eye(128, dtype="uint8")
    for i in range(n_bits):
        res[dest_start+i, source_start+i] ^= 1

    return res

S0, S1 = 0, 64

# uint64_t s1 = *state0;
# uint64_t s0 = *state1;
# *state0 = s0;
# s1 ^= s1 << 23;
# s1 ^= s1 >> 17;
# s1 ^= s0;
# s1 ^= s0 >> 26;
# *state1 = s1;

# eq to

# swap(s0, s1)
# s1 ^= s1 << 23;
# s1 ^= s1 >> 17;
# s1 ^= s0;
# s1 ^= s0 >> 26;

def compose(*xs):
    res = np.eye(128, dtype="uint8")
    for x in xs:
        res = (x @ res) & 1
    return res

def apply(m, x):
    return (m @ x) & 1

l0 = np.vstack((
    np.hstack((np.zeros((64, 64)), np.eye(64))),
    np.hstack((np.eye(64), np.zeros((64, 64)))),
))
l0 = np.array(l0, "uint8")

l1 = xor_op(S1 + 23, S1, 64 - 23)
l2 = xor_op(S1, S1 + 17, 64 - 17)

l3 = xor_op(S1, S0, 64)
l4 = xor_op(S1, S0 + 26, 64 - 26)

xorshift128 = compose(l0, l1, l2, l3, l4)

if __name__ == "__main__":

    print("numeric:", xorshift128_n(123, 321))
    print(" linalg:", vec_state(apply(xorshift128, state_vec(123, 321))))

# bit 63 of S0 after repeating xorshift128 n times
xorshift_top_bit_repeated = np.zeros((0, 128), dtype="uint8")

current = np.eye(128, dtype="uint8")
for i in range(128):
    xorshift_top_bit_repeated = np.vstack((
        xorshift_top_bit_repeated,
        current[S0 + 63, :].reshape(1, 128),
    ))

    current = (xorshift128 @ current) & 1

def find_st(s0_63_seq):
    wanted = np.array(s0_63_seq, dtype="uint8")
    init_state = solve(xorshift_top_bit_repeated, wanted)
    st = vec_state(init_state)
    st = (int(st[0]), int(st[1]))
    return st

if __name__ == "__main__":
    if PLOT:
        # pretty pictures :3
        fig, (ax_xorshift, ax_rep) = plt.subplots(2)
        ax_xorshift.imshow(xorshift128)
        ax_rep.imshow(xorshift_top_bit_repeated)
        fig.show()
        plt.show()

    wanted = np.zeros((128, ), dtype="uint8")
    wanted[1] = 1
    init_state = solve(xorshift_top_bit_repeated, wanted)
    print(init_state)
    st = vec_state(init_state)
    print(st)
    st = (int(st[0]), int(st[1]))
    for i in range(128):
        print(st[0] >> 63, end=", ")
        st = xorshift128_n(*st)
