from hashlib import md5

FLAG = 'SSM{70ld_y0u_17_w45_fr33}'

with open('chall.txt', 'w') as f:
    f.writelines([md5(x.encode()).hexdigest() + '\n' for x in FLAG])
