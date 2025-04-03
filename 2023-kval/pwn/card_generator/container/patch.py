from pathlib import Path

try:
    print("Vilken byte vill du patcha? (i hex)")
    address = int(input(), 16)
    print("Vad vill du patcha den till? (i hex)")
    byte = int(input()[:2], 16)
except ValueError:
    print("Invalid hex!")
    exit(1)

binary = list(Path("service").read_bytes())

if not 0 <= address < len(binary):
    print("Adressen är utanför binären!")
    exit(1)

binary[address] = byte
Path("/tmp/patched").write_bytes(bytes(binary))

print("Här kommer den patchade binären:")
