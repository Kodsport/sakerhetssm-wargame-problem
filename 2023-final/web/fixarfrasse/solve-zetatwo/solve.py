#!/usr/bin/env python3

import requests

BASE_URL = 'http://localhost:5000'

with open('../src/vuln/index.php', 'r') as fin:
    vuln_file = fin.read()

with open('patched.php', 'r') as fin:
    patched_file = fin.read()

r = requests.post(BASE_URL + '/evaluate', files = {'file': ('index.php', vuln_file)})
print(r.text)

r = requests.post(BASE_URL + '/evaluate', files = {'file': ('index.php', patched_file)})
print(r.text)