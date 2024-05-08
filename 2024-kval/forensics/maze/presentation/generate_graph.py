import struct
import graphviz


# tack xenia
def parse_entry(f, N):
    f.seek(0x14200 + 0x200 * (N - 2))
    d = f.read(0x200)
    entries = struct.unpack(
        "11sxxxxxxxxxxxxxxxHxxxx" * 16,
        d,
    )
    entries = zip(entries[::2], entries[1::2])

    return [(e[0].rstrip(), e[1]) for e in entries if e[0] != b"\x00" * 11]


seen_nodes = set()
seen_edges = set()
graph = graphviz.Graph(graph_attr={"overlap": "false"}, edge_attr={"len": "0.3"})
graph.node("2", label="S")

with open("../filesystem", "rb") as f:
    for i in range(31000 + 3):
        entries = parse_entry(f, i)
        if not entries:
            continue
        if entries[0][0] != b".":
            continue
        entries = entries[2:]
        print(entries)

        for entry in entries:
            if entry[1] not in seen_nodes:
                seen_nodes.add(entry[1])
                print(repr(entry[0].decode()))
                graph.node(str(entry[1]), label=entry[0].decode())
            edge = tuple(sorted((str(entry[1]), str(i))))
            if edge not in seen_edges:
                seen_edges.add(edge)
                graph.edge(*edge, len="0.3")

graph.render("graph2", engine="neato", format="pdf")
graph.render("graph2", engine="neato", format="png")
graph.render("graph2", engine="neato")
