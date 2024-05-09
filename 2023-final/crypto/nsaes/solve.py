import numpy as np
import sys

if len(sys.argv) > 1 and sys.argv[1] == "geni":
    print("echo '", end="")
    print(hex(0)[2:].ljust(32, "0"), end="\\n")
    for i in range(128):
        print(hex(1<<i)[2:].rjust(32, "0"), end="\\n")
    print("' | nc ...")
    exit(0)


session = """\
** Welcome to NSAES, the non-backdoored© AES variant **
Here is the encrypted flag. Good luck decrypting it!
8a0c2fb0e3fb9887def638bb7637e8f0
Please enter a string to be encrypted
Here is your encrypted string: 0c273d0d5f07c1689c29c634dd85b8ef
Please enter a string to be encrypted
Here is your encrypted string: 0c1f3e397207e66a9d11c600f0849fef
Please enter a string to be encrypted
Here is your encrypted string: 0c573b6505078f6c9e59c65c8787f6ef
Please enter a string to be encrypted
Here is your encrypted string: 0cc731ddeb075d6098c9c6e4698124ef
Please enter a string to be encrypted
Here is your encrypted string: 0cfc25b62c07e27894f2c68fae8d9bef
Please enter a string to be encrypted
Here is your encrypted string: 0c8a0d60b90787488c84c6593b95feef
Please enter a string to be encrypted
Here is your encrypted string: 0c665dd788074d28bc68c6ee0aa534ef
Please enter a string to be encrypted
Here is your encrypted string: 0ca5fda2ea07c2e8dcabc69b68c5bbef
Please enter a string to be encrypted
Here is your encrypted string: 0c38a6482e07c7731c36c671ac05beef
Please enter a string to be encrypted
Here is your encrypted string: 3427090c5e20c145a42af234dda2bac2
Please enter a string to be encrypted
Here is your encrypted string: 7c27550f5d49c132ec2fae34ddcbbcb5
Please enter a string to be encrypted
Here is your encrypted string: ec27ed095b9bc1dc7c251634dd19b05b
Please enter a string to be encrypted
Here is your encrypted string: d72786055724c11b47317d34dda6a89c
Please enter a string to be encrypted
Here is your encrypted string: a127501d4f41c18e3119ab34ddc39809
Please enter a string to be encrypted
Here is your encrypted string: 4d27e72d7f8bc1bfdd491c34dd09f838
Please enter a string to be encrypted
Here is your encrypted string: 8e27924d1f04c1dd1ee96934dd86385a
Please enter a string to be encrypted
Here is your encrypted string: 1327788ddf01c11983b28334dd83a39e
Please enter a string to be encrypted
Here is your encrypted string: 0f133d357805ec689c1dc70cfa8595ee
Please enter a string to be encrypted
Here is your encrypted string: 0a4f3d7d11039b689c41c4449385e2ed
Please enter a string to be encrypted
Here is your encrypted string: 00f73dedc30f75689cf9c2d441850ceb
Please enter a string to be encrypted
Here is your encrypted string: 149c3dd67c17b2689c92ceeffe85cbe7
Please enter a string to be encrypted
Here is your encrypted string: 3c4a3da0192727689c44d6999b855eff
Please enter a string to be encrypted
Here is your encrypted string: 6cfd3d4cd34716689cf3e67551856fcf
Please enter a string to be encrypted
Here is your encrypted string: cc883d8f5c8774689c8686b6de850daf
Please enter a string to be encrypted
Here is your encrypted string: 97623d12591cb0689c6c462bdb85c96f
Please enter a string to be encrypted
Here is your encrypted string: 3826050d5f2ac04fa829fe37dfa8b8c8
Please enter a string to be encrypted
Here is your encrypted string: 64254d0d5f5dc326f429b632d9dfb8a1
Please enter a string to be encrypted
Here is your encrypted string: dc23dd0d5fb3c5f44c292638d531b873
Please enter a string to be encrypted
Here is your encrypted string: b72fe60d5f74c94b27291d2ccdf6b8cc
Please enter a string to be encrypted
Here is your encrypted string: 6137900d5fe1d12ef1296b04fd63b8a9
Please enter a string to be encrypted
Here is your encrypted string: d6077c0d5fd0e1e4462987549d52b863
Please enter a string to be encrypted
Here is your encrypted string: a367bf0d5fb2816b332944f45d30b8ec
Please enter a string to be encrypted
Here is your encrypted string: 49a7220d5f76416ed929d9afc6f4b8e9
Please enter a string to be encrypted
Here is your encrypted string: 21271a0f5e3fc15cb128e134ddbdbbdb
Please enter a string to be encrypted
Here is your encrypted string: 562773095d77c100c62b8834ddf5be87
Please enter a string to be encrypted
Here is your encrypted string: b827a1055be7c1b8282d5a34dd65b43f
Please enter a string to be encrypted
Here is your encrypted string: 7f271e1d57dcc1d3ef21e534dd5ea054
Please enter a string to be encrypted
Here is your encrypted string: ea277b2d4faac1057a398034dd288882
Please enter a string to be encrypted
Here is your encrypted string: db27b14d7f46c1b24b094a34ddc4d835
Please enter a string to be encrypted
Here is your encrypted string: b9273e8d1f85c1c72969c534dd077840
Please enter a string to be encrypted
Here is your encrypted string: 7d273b16df18c12deda9c034dd9a23aa
Please enter a string to be encrypted
Here is your encrypted string: 0d003d206704f5689c0ec419e5858cee
Please enter a string to be encrypted
Here is your encrypted string: 0e693d572f01a9689c67c26ead85d0ed
Please enter a string to be encrypted
Here is your encrypted string: 08bb3db9bf0b11689cb5ce803d8568eb
Please enter a string to be encrypted
Here is your encrypted string: 04043d7e841f7a689c0ad647068503e7
Please enter a string to be encrypted
Here is your encrypted string: 1c613debf237ac689c6fe6d27085d5ff
Please enter a string to be encrypted
Here is your encrypted string: 2cab3dda1e671b689ca586e39c8562cf
Please enter a string to be encrypted
Here is your encrypted string: 4c243db8ddc76e689c2a46815f8517af
Please enter a string to be encrypted
Here is your encrypted string: 8c213d7c409c84689c2fdd45c285fd6f
Please enter a string to be encrypted
Here is your encrypted string: 2b25100d5f33c050bb29eb35deb1b8d7
Please enter a string to be encrypted
Here is your encrypted string: 4223670d5f6fc318d2299c36dbedb89f
Please enter a string to be encrypted
Here is your encrypted string: 902f890d5fd7c58800297230d155b80f
Please enter a string to be encrypted
Here is your encrypted string: 2f374e0d5fbcc9b3bf29b53cc53eb834
Please enter a string to be encrypted
Here is your encrypted string: 4a07db0d5f6ad1c5da292024ede8b842
Please enter a string to be encrypted
Here is your encrypted string: 8067ea0d5fdde12910291114bd5fb8ae
Please enter a string to be encrypted
Here is your encrypted string: 0fa7880d5fa881ea9f2973741d2ab86d
Please enter a string to be encrypted
Here is your encrypted string: 0a3c4c0d5f4241779a29b7b446c0b8f0
Please enter a string to be encrypted
Here is your encrypted string: 0c0a3c2a6b07f96b9e04c613e98480ef
Please enter a string to be encrypted
Here is your encrypted string: 0c7d3f433707b16e9873c67ab587c8ef
Please enter a string to be encrypted
Here is your encrypted string: 0c9339918f072164949dc6a80d8158ef
Please enter a string to be encrypted
Here is your encrypted string: 0c54352ee4071a708c5ac617668d63ef
Please enter a string to be encrypted
Here is your encrypted string: 0cc12d4b32076c58bccfc672b09515ef
Please enter a string to be encrypted
Here is your encrypted string: 0cf01d8185078008dcfec6b807a5f9ef
Please enter a string to be encrypted
Here is your encrypted string: 0c927d0ef00743a81c9cc63772c53aef
Please enter a string to be encrypted
Here is your encrypted string: 0c56bd0b1a07def38758c6329805a7ef
Please enter a string to be encrypted
Here is your encrypted string: 0d1f3d397206e6689c11c500f0859fed
Please enter a string to be encrypted
Here is your encrypted string: 0e573d6505058f689c59c05c8785f6eb
Please enter a string to be encrypted
Here is your encrypted string: 08c73dddeb035d689cc9cae4698524e7
Please enter a string to be encrypted
Here is your encrypted string: 04fc3db62c0fe2689cf2de8fae859bff
Please enter a string to be encrypted
Here is your encrypted string: 1c8a3d60b91787689c84f6593b85fecf
Please enter a string to be encrypted
Here is your encrypted string: 2c663dd788274d689c68a6ee0a8534af
Please enter a string to be encrypted
Here is your encrypted string: 4ca53da2ea47c2689cab069b6885bb6f
Please enter a string to be encrypted
Here is your encrypted string: 8c383d482e87c7689c365d71ac85bef4
Please enter a string to be encrypted
Here is your encrypted string: 3424090d5f20c345a429f235dca2b8c2
Please enter a string to be encrypted
Here is your encrypted string: 7c21550d5f49c532ec29ae36dfcbb8b5
Please enter a string to be encrypted
Here is your encrypted string: ec2bed0d5f9bc9dc7c291630d919b85b
Please enter a string to be encrypted
Here is your encrypted string: d73f860d5f24d11b47297d3cd5a6b89c
Please enter a string to be encrypted
Here is your encrypted string: a117500d5f41e18e3129ab24cdc3b809
Please enter a string to be encrypted
Here is your encrypted string: 4d47e70d5f8b81bfdd291c14fd09b838
Please enter a string to be encrypted
Here is your encrypted string: 8ee7920d5f0441dd1e2969749d86b85a
Please enter a string to be encrypted
Here is your encrypted string: 13bc780d5f01da19832983b45d83b89e
Please enter a string to be encrypted
Here is your encrypted string: 0c133c357807ec699f1dc60cfa8795ef
Please enter a string to be encrypted
Here is your encrypted string: 0c4f3f7d11079b6a9a41c6449381e2ef
Please enter a string to be encrypted
Here is your encrypted string: 0cf739edc307756c90f9c6d4418d0cef
Please enter a string to be encrypted
Here is your encrypted string: 0c9c35d67c07b2608492c6effe95cbef
Please enter a string to be encrypted
Here is your encrypted string: 0c4a2da019072778ac44c6999ba55eef
Please enter a string to be encrypted
Here is your encrypted string: 0cfd1d4cd3071648fcf3c67551c56fef
Please enter a string to be encrypted
Here is your encrypted string: 0c887d8f5c0774285c86c6b6de050def
Please enter a string to be encrypted
Here is your encrypted string: 0c62bd125907b0e8076cc62bdb9ec9ef
Please enter a string to be encrypted
Here is your encrypted string: 3827050e5d2ac14fa828fe34dda8b9c8
Please enter a string to be encrypted
Here is your encrypted string: 64274d0b5b5dc126f42bb634dddfbaa1
Please enter a string to be encrypted
Here is your encrypted string: dc27dd0157b3c1f44c2d2634dd31bc73
Please enter a string to be encrypted
Here is your encrypted string: b727e6154f74c14b27211d34ddf6b0cc
Please enter a string to be encrypted
Here is your encrypted string: 6127903d7fe1c12ef1396b34dd63a8a9
Please enter a string to be encrypted
Here is your encrypted string: d6277c6d1fd0c1e446098734dd529863
Please enter a string to be encrypted
Here is your encrypted string: a327bfcddfb2c16b33694434dd30f8ec
Please enter a string to be encrypted
Here is your encrypted string: 492722964476c16ed9a9d934ddf438e9
Please enter a string to be encrypted
Here is your encrypted string: 21261a0d5f3fc25cb129e136dcbdb8db
Please enter a string to be encrypted
Here is your encrypted string: 5625730d5f77c700c6298830dff5b887
Please enter a string to be encrypted
Here is your encrypted string: b823a10d5fe7cdb828295a3cd965b83f
Please enter a string to be encrypted
Here is your encrypted string: 7f2f1e0d5fdcd9d3ef29e524d55eb854
Please enter a string to be encrypted
Here is your encrypted string: ea377b0d5faaf1057a298014cd28b882
Please enter a string to be encrypted
Here is your encrypted string: db07b10d5f46a1b24b294a74fdc4b835
Please enter a string to be encrypted
Here is your encrypted string: b9673e0d5f8501c72929c5b49d07b840
Please enter a string to be encrypted
Here is your encrypted string: 7da73b0d5f185a2ded29c02f5d9ab8aa
Please enter a string to be encrypted
Here is your encrypted string: 0c003f206707f5699d0ec619e5868cef
Please enter a string to be encrypted
Here is your encrypted string: 0c6939572f07a96a9e67c66ead83d0ef
Please enter a string to be encrypted
Here is your encrypted string: 0cbb35b9bf07116c98b5c6803d8968ef
Please enter a string to be encrypted
Here is your encrypted string: 0c042d7e84077a60940ac647069d03ef
Please enter a string to be encrypted
Here is your encrypted string: 0c611debf207ac788c6fc6d270b5d5ef
Please enter a string to be encrypted
Here is your encrypted string: 0cab7dda1e071b48bca5c6e39ce562ef
Please enter a string to be encrypted
Here is your encrypted string: 0c24bdb8dd076e28dc2ac6815f4517ef
Please enter a string to be encrypted
Here is your encrypted string: 0c21267c400784e81c2fc645c21efdef
Please enter a string to be encrypted
Here is your encrypted string: 2b27100c5c33c150bb2beb34ddb1b9d7
Please enter a string to be encrypted
Here is your encrypted string: 4227670f596fc118d22d9c34ddedba9f
Please enter a string to be encrypted
Here is your encrypted string: 9027890953d7c18800217234dd55bc0f
Please enter a string to be encrypted
Here is your encrypted string: 2f274e0547bcc1b3bf39b534dd3eb034
Please enter a string to be encrypted
Here is your encrypted string: 4a27db1d6f6ac1c5da092034dde8a842
Please enter a string to be encrypted
Here is your encrypted string: 8027ea2d3fddc12910691134dd5f98ae
Please enter a string to be encrypted
Here is your encrypted string: 0f27884d9fa8c1ea9fa97334dd2af86d
Please enter a string to be encrypted
Here is your encrypted string: 0a274c8dc442c1779a32b734ddc038f0
Please enter a string to be encrypted
Here is your encrypted string: 0e0a3d2a6b06f9689c04c713e98580ec
Please enter a string to be encrypted
Here is your encrypted string: 087d3d433705b1689c73c47ab585c8e9
Please enter a string to be encrypted
Here is your encrypted string: 04933d918f0321689c9dc2a80d8558e3
Please enter a string to be encrypted
Here is your encrypted string: 1c543d2ee40f1a689c5ace17668563f7
Please enter a string to be encrypted
Here is your encrypted string: 2cc13d4b32176c689ccfd672b08515df
Please enter a string to be encrypted
Here is your encrypted string: 4cf03d81852780689cfee6b80785f98f
Please enter a string to be encrypted
Here is your encrypted string: 8c923d0ef04743689c9c863772853a2f
Please enter a string to be encrypted
Here is your encrypted string: 17563d0b1a87de689c5846329885a774
Please enter a string to be encrypted
Need a hex string of 16 bytes
"""

def tovec(x):
    b = bytes.fromhex(x)
    bits = [(byte >> i) & 1 for byte in b for i in range(8)]
    return np.array(bits).reshape(128, 1)

session = session.split("\n")
offset = tovec(session[4].split(": ", 1)[1])
print("offset =", offset.flatten())

flag_enc = offset ^ tovec(session[2])
print("flag =", flag_enc.flatten())

bases = np.concatenate([offset ^ tovec(session[2*i+6].split(": ", 1)[1]) for i in range(128)], axis=1)

print(bases.shape)
print(bases)


# from my solve script of SHA (kval)
# finds an x such that A @ x = b
# gaussian elimination
def solve(A, b):
    M = np.hstack((A, b[:, np.newaxis]))

    for col in range(128):
        pivot_row = -1
        for row in range(col, 128):
            if M[row, col] == 1:
                pivot_row = row
                break

        if pivot_row == -1:
            raise ValueError(f"Singular matrix 3: (got to col {col})")

        row_content = np.copy(M[pivot_row])
        M[pivot_row] = M[col]
        M[col] = row_content

        for row in range(128):
            if row == col:
                continue

            if M[row, col] == 1:
                M[row, :] ^= row_content

    return M[:, 128]

flag_dec = solve(bases, flag_enc.flatten())
flag_bytes = (flag_dec.reshape(16, 8) * 2**np.arange(8)).sum(axis=1)

print(bytes(list(flag_bytes))[::-1].decode())
