#!/usr/bin/env python3
import random

random.seed(123456)

flag = "SSM{th!5_sh0u1d_h4v3_b3en_in_PO}"

n = len(flag)

# Generate a random tree
parents = [random.randint(0,i) for i in range(n-1)]
edges = [[] for _ in range(n)]
for u,v in enumerate(parents):
    edges[u+1].append(v)
    edges[v].append(u+1)

for nei in edges:
    nei.sort(reverse=1) 

# Simulate the Squirrel's movement (it loves big numbers, so when faced a choice during the traversal, it will visit bigger indicies before other choices)
flagIdx = 0
visited = [0]*n
piece = ["" for _ in range(n)]
def DFS(curr):

    global flagIdx

    for nei in edges[curr]:
        if not visited[nei]:
            visited[nei] = 1
            DFS(nei)

    piece[curr] = flag[flagIdx]
    flagIdx += 1

visited[0] = 1
DFS(0)
assert flagIdx == n

degrees = [len(adjs) for adjs in edges]

def XORall(a):
    temp = 0
    for x in a:
        temp ^= x
    return temp

XOR = [XORall(adjs) for adjs in edges]


#pypy3 maketree.py > tree.txt
print(degrees)
print(XOR)
print(piece)

