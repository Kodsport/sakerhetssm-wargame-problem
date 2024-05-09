import struct

flag_encryption = "edf8382a3ddb7677e7e3b6e0a386dc5c22b5d4e929480e439cd7f5d21c74f4489cf462b0fb9684205f00eb2f0684206e5a4cc38b0684205c60b1ba8b068420"

inp = b'meowmeowmeowmeow'.ljust(64)
enc = "1cc3c217fc69e14dee777217fc69e14dff74177a8b0684207674177a8b0684203674177a8b0684203674177a8b0684203674177a8b0684203674177a8b068420"

inp_nums = struct.unpack("8Q", inp)
enc_nums = struct.unpack(">8Q", bytes.fromhex(enc))

seeds = [i ^ e for i, e in zip(inp_nums, enc_nums)]

# seeds[1] = seeds[0] ** 2 + seed_addr
seed_addr = (seeds[1] - seeds[0] ** 2) & 0xffff_ffff_ffff_ffff
print("seed @", hex(seed_addr))

for first_zero in range(0, len(flag_encryption), 8):
    for second_zero in range(first_zero, len(flag_encryption), 8):
        zeroed_flag = flag_encryption[:first_zero] + "0" + flag_encryption[first_zero:second_zero] + "0" + flag_encryption[second_zero:]

        enc_flag_nums = struct.unpack(">8Q", bytes.fromhex(zeroed_flag))

        flag = b''

        seed = 0xdeadbeefcafebabe
        for f in enc_flag_nums:
            seed = (seed ** 2 + seed_addr) & 0xffff_ffff_ffff_ffff
            flag += struct.pack("Q", f ^ seed)

        if flag.startswith(b'SSM{') and b'}\x00' in flag:
            print(flag)
