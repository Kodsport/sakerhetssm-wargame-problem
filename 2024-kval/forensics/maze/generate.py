import struct
import random
from pathlib import Path
from queue import Queue

node_count = 31000
edge_count = int(node_count * 1.4)
flag = "{V3RY_F47_CH411_GHVJF8MWPW}"

# node_count = 5
# edge_count = 8
# flag = "ABC"


fs = bytearray(Path("empty_filesystem").read_bytes())
print(len(fs))

LOC_TABLE = 0x200
LOC_ROOTDIR = 0x10200
LOC_CLUSTER2 = LOC_ROOTDIR + 512 * 32


def create_direntry(dirname, cluster):
    return (
        b"%(dirname)b   \x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%(cluster)b\x00\x00\x00\x00"
        % {
            b"dirname": struct.pack("<8s", dirname.encode()).replace(b"\x00", b"\x20"),
            b"cluster": struct.pack("<H", cluster),
        }
    )


def create_dirtable(entries, cluster, parent, extra=None):
    table = b""
    table += create_direntry(".", cluster)
    table += create_direntry("..", parent)
    for dirname, entry_cluster in entries:
        table += create_direntry(dirname, entry_cluster)
    if extra:
        table += extra
    assert len(table) <= 512
    return table


def pad(b, n):
    return b + b"\x00" * (n - len(b))


def get_furthest_node(node):
    seen = set()
    queue = Queue()
    queue.put((node, []))
    best = (None, [])
    while not queue.empty():
        state = queue.get()
        if state[0] in seen:
            continue
        seen.add(state[0])
        if len(state[1]) > len(best[1]) - 1:
            best = (state[0], state[1] + [state[0]])
        for adj_node in nodes[state[0]]:
            queue.put((adj_node, state[1] + [state[0]]))
    return *best, seen


while True:
    print("generating nodes")
    nodes = [set() for _ in range(node_count)]
    edges = set()

    for i in range(edge_count):
        while True:
            a = random.randint(0, node_count - 1)
            b = random.randint(0, node_count - 1)
            if (
                a != b
                and (a, b) not in edges
                and (b, a) not in edges
                and len(nodes[a]) < 16
                and len(nodes[b]) < 16
            ):
                break
        edges.add((a, b))
        nodes[a].add(b)
        nodes[b].add(a)

    # print(nodes)
    try:
        start_node = get_furthest_node(0)[0]
        end_node, path, seen = get_furthest_node(start_node)
    except TypeError:
        continue
    print(len(seen))
    print(start_node, end_node)
    print(path)
    print(len(path))
    if len(path) == len(flag):
        break

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"
node_names = [random.choice(alphabet) for _ in nodes]
for i, node in enumerate(path):
    node_names[node] = flag[i]

# update FAT
FAT = (
    b"\xf8\xff\xff\xff"
    + b"\xff\xff" * 4
    + b"".join([b"\xff\xff" if i in seen else b"\x00\x00" for i in range(len(nodes))])
)
fs[LOC_TABLE : LOC_TABLE + 4 + 2 * (4 + len(nodes))] = FAT

# update rootdir
fs[LOC_ROOTDIR : LOC_ROOTDIR + 0x20] = create_direntry("S", 2)

# update data
fs[LOC_CLUSTER2 : LOC_CLUSTER2 + 0x200 * (3 + len(nodes))] = (
    pad(create_dirtable([("S", 3)], 2, 0), 0x200)
    + pad(create_dirtable([("M", 4)], 3, 0), 0x200)
    + pad(create_dirtable([("{", start_node + 5)], 4, 0), 0x200)
    + b"".join(
        [
            (
                pad(
                    create_dirtable(
                        [(node_names[n], n + 5) for n in nodes[i]],
                        i + 5,
                        0,
                    ),
                    0x200,
                )
                if i in seen
                else b"\x00" * 0x200
            )
            for i in range(len(nodes))
        ]
    )
)

end_text = b"Well done, but what do you want from me? The real flag is the shortest path we made along the way..."

# overwrite end node
fs[
    LOC_CLUSTER2 + 0x200 * (3 + end_node) : LOC_CLUSTER2 + 0x200 * (3 + end_node + 1)
] = pad(
    create_dirtable(
        [(node_names[n], n + 5) for n in nodes[end_node]],
        end_node + 5,
        0,
        extra=b"flag\x20\x20\x20\x20txt\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        + struct.pack("<H", len(nodes) + 5)
        + struct.pack("<I", len(end_text)),
    ),
    0x200,
)

fs[
    LOC_CLUSTER2
    + 0x200 * (3 + len(nodes)) : LOC_CLUSTER2
    + 0x200 * (3 + len(nodes) + 1)
] = pad(end_text, 0x200)

Path("filesystem").write_bytes(fs)

print(len(fs))
