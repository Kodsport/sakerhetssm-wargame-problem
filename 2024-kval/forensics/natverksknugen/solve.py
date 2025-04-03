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
    inp: bytes = rolling_xor(base64.b64decode('ShJXaHZqHUwwZmIzI1wcL398cz4ENW8vUjY9dGk5UzxzI3I5KjAB'), b'banana')
    homework: str = open('files/home/user/Desktop/homework').read()

    pos: int = 0
    for i in range(0, 300*38, 300):
        print(chr(inp[pos] ^ ord(homework[i])), end='')

        if pos != len(inp):
            pos += 1

if __name__ == '__main__':
    main()