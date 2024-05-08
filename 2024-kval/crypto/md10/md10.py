from hashlib import md5

FLAG = b'SSM{d0nt_3v3n_try_t0_xxxxxxx_gu3ss_y0u_l1ttl3...}'

# md(5+5) = md10
a = int(md5(FLAG[:25]).hexdigest(), 16)
b = int(md5(FLAG[25:]).hexdigest(), 16)

with open('enc_flag', 'w') as f:
    f.write(str(a+b))
    f.close()
