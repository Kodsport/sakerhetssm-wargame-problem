#!/usr/bin/env python3

flag = "SSM{th!5_sh0u1d_h4v3_b3en_in_PO}"

# Adjacency list for the squirrel's neighborhood
edges = [[1, 2, 3, 4, 5, 6, 8, 14], [0, 9, 19, 21, 31], [0, 7, 13], [0, 10], [0, 16], [0, 20, 27], [0], [2, 12], [0, 15], [1], [3, 11], [10, 18], [7, 17], [2], [0, 22, 24, 25], [8], [4, 23, 26, 28], [12, 29], [11], [1], [5], [1], [14], [16], [14], [14, 30], [16], [5], [16], [17], [25], [1]]

n = len(edges)

degrees = [len(adjs) for adjs in edges]

def XORadjs(adjs):
    temp = 0
    for x in adjs:
        temp ^= x
    return temp

XOR = [XORadjs(adjs) for adjs in edges]

# Sort the adjacency list for the squirrel's preference
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

print(degrees)
print(XOR)
print(fragments)
