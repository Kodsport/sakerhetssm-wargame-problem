#!/usr/bin/env python3

import ast

with open('tree.txt', 'r') as fin:
    degrees = ast.literal_eval(next(fin))
    xoradj = ast.literal_eval(next(fin))
    fragments = ast.literal_eval(next(fin))

print(degrees)
print(xoradj)
print(fragments)

N = len(degrees)
assert len(xoradj) == N, len(xoradj)
assert len(fragments) == N, len(fragments)

adjacency = [set() for _ in range(N)]


# Reconstruct adjancency graph
while True:
    for i in range(N):
        if degrees[i] - len(adjacency[i]) != 1:
            continue

        d = 0
        for x in adjacency[i]:
            d ^= x

        other = xoradj[i] ^ d
        adjacency[i].add(other)
        adjacency[other].add(i)

    if all(degrees[i] - len(adjacency[i]) == 0 for i in range(N)):
        break

# Validate XOR
for i in range(N):
    d = 0
    for x in adjacency[i]:
        d ^= x
    if d != xoradj[i]:
        print(f'xoradj[{i}] == {xoradj[i]} != {d}')

for i in range(N):
    print(f'{i:2d} ({degrees[i]}) => {adjacency[i]}')



def calculate_tree(adjacency):
    global flagIdx
    N = len(adjacency)
    flag = [i for i in range(N)]

    # Adjacency list for the squirrel's neighborhood
    edges = [list(adjacency[i]) for i in range(N)]

    n = len(edges)

    degrees = [len(adjs) for adjs in edges]

    def XORadjs(adjs):
        temp = 0
        for x in adjs:
            temp ^= x
        return temp

    XOR = [XORadjs(adjs) for adjs in edges]

    # Sort the adjacency list according to the squirrel's preference
    for nei in edges:
        nei.sort(reverse = True) 

    flagIdx = 0
    visited = [0] * n
    fragments = ["" for _ in range(n)]

    def squirrelWalk(curr):

        global flagIdx

        for nei in edges[curr]:
            if not visited[nei]:
                visited[nei] = 1
                squirrelWalk(nei)

        # Uh oh it dropped a bit of the flag on the current node
        fragments[curr] = flag[flagIdx]

        flagIdx += 1

    visited[0] = 1

    squirrelWalk(0)

    return degrees, XOR, fragments


calc_degrees, calc_xor, calc_fragments = calculate_tree(adjacency)

print(calc_degrees == degrees, calc_degrees)
print(calc_xor == xoradj, calc_xor)
print(calc_fragments)
print(fragments)
flag = ''.join(fragments[calc_fragments.index(x)] for x in range(len(calc_degrees)))
print(f'Flag: {flag}')
