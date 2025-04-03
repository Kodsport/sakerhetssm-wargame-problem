#!/usr/bin/env python3

import sys
import json

HASH_LEN = int(sys.argv[1])
F = GF(2^8)

rand_mat = random_matrix(F, HASH_LEN)

rand_mat_n = [[x.integer_representation() for x in row] for row in rand_mat]
rand_mat_inv_n = [[x.integer_representation() for x in row] for row in rand_mat.inverse()]

m = int(sum(Integer(i) * (2^Integer(e)) for e, i in enumerate(F.modulus().list())))

print(json.dumps({
    'mod': m,
    'matrix': rand_mat_n,
    'matrix_inv': rand_mat_inv_n
}))
