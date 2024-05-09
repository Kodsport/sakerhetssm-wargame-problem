# WTF linear algebra
"""Anti-rolling-hash test generation by lattice reduction
original code by Hellman_, modified by dacin21
"""

from sage.all import *

def anti_hash(PAs, string_length, sigma, block_size = 0, MULTIPLIER = 100000, sigma_base = ord('a')):
    n = len(PAs)
    N = string_length
    As = [a for p, a in PAs]
    Ps = [p for p, a in PAs]

    def h(s):
        """polynomial hash modulo <n> primes"""
        v = [0] * n
        for c in s:
            v = [(x * q + ord(c))%p for x, q, p in zip(v, As, Ps)]
        return tuple(v % p for v, p in zip(v, Ps))

    mv = matrix(ZZ, N, N)
    for y in range(N):
        for x, q, p in zip(range(n), As, Ps):
            mv[y,x] = pow(q, N-y-1, p);

    m = matrix(ZZ, N + n, N + n)
    # submatrix with terms
    m.set_block(0, 0, MULTIPLIER * mv)
    # modulo reductions
    m.set_block(N, 0, MULTIPLIER * diagonal_matrix(Ps))
    # term coefficients
    m.set_block(0, n, identity_matrix(N))
    # 4th submatrix is zero

    m_reduced = m.LLL()
    if block_size > 0:
        m_reduced = m_reduced.BKZ(block_size = block_size)

    for row in m_reduced:
        print(row[:n], min(row[n:]), "~", max(row[n:]))
        delta = max(abs(v) for v in row[n:])
        if set(row[:n]) == {0} and delta < sigma:
            print("Found collision!")
            s = [None] * N
            t = [None] * N
            for i, v in enumerate(row[n:]):
                a = sigma_base
                b = a + abs(v)
                if v > 0:
                    a, b = b, a
                s[i] = a
                t[i] = b
            s = "".join(map(chr, s))
            t = "".join(map(chr, t))
            
            print(s[::-1])
            print(t[::-1])
            print(h(s))
            print(h(t))
            assert h(s) == h(t)
            break
    else:
        print("Failed to find collision, try a larger string_length")
        print("For lengths > 30, setting block_size to 10 or 15 is recommended")

if __name__ == '__main__':
    k, sigma = 25, 26
    PAs = [(2097143 , 7610), (2097143 , 27116), (2097143 , 18775)]

    anti_hash(PAs, k, sigma)
