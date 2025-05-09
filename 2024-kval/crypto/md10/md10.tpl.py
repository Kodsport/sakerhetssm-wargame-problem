from hashlib import md5

FLAG = b'FLAG_PLACEHOLDER'

# md(5+5) = md10
a = int(md5(FLAG[:25]).hexdigest(), 16)
b = int(md5(FLAG[25:]).hexdigest(), 16)

with open('enc_flag', 'w') as f:
    f.write(str(a+b))
    f.close()
