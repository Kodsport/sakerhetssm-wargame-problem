C = 0xe6

for i in range(256):
    if i % 16 == 0:
        print("    ", end="")
    print(f"0x{i^C:02x}, ", end="")
    if i % 16 == 15:
        print("\n", end="")
