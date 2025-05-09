import socket
import base64

def rolling_xor(msg: bytes, key: bytes) -> bytes:
    enc: bytearray = []
    pos: int = 0

    for b in msg:
        if pos == len(key):
            pos = 0

        enc.append(b ^ key[pos])
        pos += 1
    return bytes(enc)

def main() -> None:
    spicy:    str = open('/flag.txt').read()
    homework: str = open('/home/user/Desktop/homework').read()

    spicy_homework: bytes = []
    i: int = 0
    for c in spicy:
        spicy_homework.append(ord(c) ^ ord(homework[i]))
        i += 300

    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 1337))
    s.listen(1)

    while True:
        client, ip = s.accept()
        client.send(f'Welcome to the server {ip[0]}:{ip[1]}!\n'.encode('ascii'))

        buffer: bytes = client.recv(64)[:-1]
        client.send(base64.b64encode(rolling_xor(spicy_homework, buffer)))

        client.close()

if __name__ == '__main__':
    main()