#!/usr/bin/env python3

import pathlib
import random
import shutil
import string
import struct
import sys

import arc4
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from jinja2 import Environment, FileSystemLoader, select_autoescape

jijnja_env = Environment(loader=FileSystemLoader("."),
                         autoescape=select_autoescape())


def generate_graph(num_nodes, min_paths, max_paths):
    num_attempts = 100
    for _ in range(num_attempts):
        graph = nx.dual_barabasi_albert_graph(num_nodes, 3, 5, 0.4)
        #graph = nx.gnp_random_graph(10,0.5,directed=True)
        graph = nx.DiGraph([(u, v) for (u, v) in graph.edges() if u < v])
        for sink in [
                node for node, out_degree in graph.out_degree
                if out_degree == 0
        ]:
            graph.add_edge(sink, num_nodes)

        paths = list(nx.all_simple_paths(graph, 0, num_nodes))
        num_paths = len(paths)
        if num_paths in range(min_paths, max_paths):
            return graph, num_paths, random.choice(paths)

    raise RuntimeError(
        f'Failed to generate graph after {num_attempts} attempts')


def generate_nodes(graph):
    nodedir = pathlib.Path('nodes')
    if nodedir.is_dir():
        shutil.rmtree(nodedir)
    nodedir.mkdir(exist_ok=False)
    node_tpl_c = jijnja_env.get_template('node.c.j2')
    node_tpl_h = jijnja_env.get_template('node.h.j2')

    keys = {}
    for node_id in graph:
        node_key = random.randrange(0, 0x10000000000000000)
        keys[node_id] = node_key
        edges = list(graph.successors(node_id))
        #print('Out:', edges)
        node_c = node_tpl_c.render(node_id=node_id,
                                   node_key=node_key,
                                   edges=edges)
        node_h = node_tpl_h.render(node_id=node_id)
        (nodedir / f'node{node_id}.h').write_text(node_h)
        (nodedir / f'node{node_id}.c').write_text(node_c)

    return keys


def generate_password(graph, solution):
    password = []
    assert solution[0] == 0
    while len(solution) > 0:
        prev, solution = solution[0], solution[1:]
        for letter, edge in zip(string.ascii_uppercase,
                                graph.successors(prev)):
            if edge == solution[0]:
                password.append(letter)
                break
    password = ''.join(password)
    return password


def calculate_target_hash(solution, keys):
    state = 0x1337133713371337
    for node in solution:
        value = keys[node]
        print(f'{node}: {state:#x}<-{value:#x}')
        state = ((
            (((state * 0x1fffffffffffffff) & 0xFFFFFFFFFFFFFFFF) + value)
            & 0xFFFFFFFFFFFFFFFF) % 0xffffffffffffffc5) & 0xFFFFFFFFFFFFFFFF
    return state


flag = sys.argv[1]

NUM_PATHS = (200, 100_000, 1_000_000)
#NUM_PATHS = (10, 10, 1000)

graph, num_paths, solution = generate_graph(*NUM_PATHS)
print(f'Num paths: {num_paths}')
write_dot(graph, "graph.dot")
print(f'Path: {solution}')
keys = generate_nodes(graph)
target_hash = calculate_target_hash(solution, keys)
print(f'Target hash: {target_hash:#x}')
password = generate_password(graph, solution)
print(f'Password: {password}')

rc4 = arc4.ARC4(struct.pack('<Q', target_hash))
ciphertext = rc4.encrypt(struct.pack('<Q', 0x1337133713371337) + flag.encode())
ciphertext_hex = ', '.join(f'{x:#02x}' for x in ciphertext)

flag_tpl_c = jijnja_env.get_template('flag.c.j2')
flag_tpl_h = jijnja_env.get_template('flag.h.j2')
with open('flag.h', 'w') as fout:
    fout.write(flag_tpl_h.render())
with open('flag.c', 'w') as fout:
    fout.write(
        flag_tpl_c.render(flag_len=len(ciphertext), flag_enc=ciphertext_hex))
