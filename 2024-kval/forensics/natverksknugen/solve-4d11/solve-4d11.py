# import socket
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

# def main() -> None:
#     spicy:    str = open('/flag.txt').read()
#     homework: str = open('/home/user/Desktop/homework').read()

#     spicy_homework: bytes = []
#     i: int = 0
#     for c in spicy:
#         spicy_homework.append(ord(c) ^ ord(homework[i]))
#         i += 300

#     s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('192.168.100.130', 1337))
#     s.listen(1)

#     while True:
#         client, ip = s.accept()
#         client.send(f'Welcome to the server {ip[0]}:{ip[1]}!\n'.encode('ascii'))

#         buffer: bytes = client.recv(64)[:-1]
#         client.send(base64.b64encode(rolling_xor(spicy_homework, buffer)))

#         client.close()

# if __name__ == '__main__':
#     main()


buffer = 0x62616e616e610a.to_bytes(7)[:-1] #BANANANANNANANNANANANANANAN

recv_spicy_homework = 0x53684a5861485a71485577775a6d497a493177634c333938637a34454e573876556a593964476b35557a787a493349354b6a4142.to_bytes(52)
recv_spicy_homework = base64.b64decode(recv_spicy_homework)
spicy_homework = rolling_xor(recv_spicy_homework, buffer).decode()

"""
extraherar homework från wireshark: File -> Export Objects -> FTP-DATA...
"""

with open("homework", "r") as file:
    homework = file.read()

spicy = []
i = 0
for c in spicy_homework:
    spicy.append(ord(c) ^ ord(homework[i]))
    i+=300

print("".join(chr(c) for c in spicy))
