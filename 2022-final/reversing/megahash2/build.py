#!/usr/bin/env python3

import json
import os
import subprocess

HASH_LEN = 32

with open('megahash.js.tpl', 'r') as fin:
    megahash_template = fin.read()
with open('solution.js.tpl', 'r') as fin:
    solution_template = fin.read()
with open('build.js.tpl', 'r') as fin:
    build_template = fin.read()
with open('challenge.js.tpl', 'r') as fin:
    challenge_template = fin.read()

parameters = json.loads(subprocess.check_output(['sage', 'generate_parameters.sage', str(HASH_LEN)]).decode())
rand_mat_n_js = '],\n\t['.join(', '.join(f'{x:#04x}' for x in row) for row in parameters['matrix'])
rand_mat_inv_n_js = '],\n\t['.join(', '.join(f'{x:#04x}' for x in row) for row in parameters['matrix_inv'])

chall_params = f'const M = {parameters["mod"]}\nconst MBOX = [\n\t[{rand_mat_n_js}]\n];'
megahash = megahash_template.replace('/*[PARAMETERS]*/', chall_params)


build = megahash + build_template
with open('build.js', 'w') as fout:
    fout.write(build)

target_hash = json.loads(subprocess.check_output(['node', 'build.js']).decode())
target_hash_js = f'const TARGET = [{", ".join(f"{x:#04x}" for x in target_hash)}]'

solution_params = f'const MBOX_INV = [\n\t[{rand_mat_inv_n_js}]\n];'
solution = megahash + solution_template.replace('/*[PARAMETERS]*/', solution_params).replace('/*[TARGET]*/', target_hash_js)

challenge = megahash + challenge_template.replace('/*[TARGET]*/', target_hash_js)

with open(os.path.join('container', 'html', 'megahash.js'), 'w') as fout:
    fout.write(challenge)

with open('solution.js', 'w') as fout:
    fout.write(solution)
