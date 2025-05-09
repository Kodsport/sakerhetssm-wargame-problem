#!/usr/bin/env python3

degrees = [8, 5, 3, 2, 2, 3, 1, 2, 2, 1, 2, 2, 2, 1, 4, 1, 4, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1]
XOR = [1, 16, 10, 10, 16, 15, 0, 14, 15, 1, 8, 24, 22, 2, 23, 8, 21, 17, 11, 1, 5, 1, 14, 16, 14, 16, 16, 5, 16, 17, 25, 1]
flagPieces = ['}', 'O', '_', '3', '_', 'h', '5', 'n', '!', 'P', 'v', '4', 'e', '_', 't', 'h', 'd', '3', 'h', '_', 's', 'n', '{', '1', 'M', 'S', 'u', '_', '0', 'b', 'S', 'i']

# We realize that the first array could be the degrees of every node in the tree.
# The second array is the XOR of all neighbors.
# The third array is the character exisiting on each of the nodes.

n = len(degrees)

edges = [[] for _ in range(n)]


# We can recreate the tree by starting from the leaves, the nodes with degree 1
BFS = []
for i,deg in enumerate(degrees):
    if deg == 1:
        BFS.append(i)

for idx in BFS:
    edges[idx].append(XOR[idx])
    edges[XOR[idx]].append(idx)
    
    degrees[idx] -= 1
    degrees[XOR[idx]] -= 1

    if degrees[XOR[idx]] == 1:
        BFS.append(XOR[idx])

    XOR[XOR[idx]] ^= idx
    XOR[idx] ^= XOR[idx] # Samma sak som att sätta det till 0.


# We sort the adj list of every node from largest to smallest
for adj in edges:
    adj.sort(reverse=1)


# We use post-order traversal to recreate the tree
def DFS(curr):
    global flag

    for nei in edges[curr]:
        if not visited[nei]:
            visited[nei] = 1
            DFS(nei)

    flag += flagPieces[curr]

    return flag


for i in range(n):
    visited = [0]*n
    visited[i] = 1
    flag = ""
    DFS(i)

    print(flag)
    if flag[:3] == "SSM":
        break

