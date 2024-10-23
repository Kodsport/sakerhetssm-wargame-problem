import sys

lines = sys.stdin.readlines()[6:]
lines = [line for line in lines if line and ">:" not in line and line != "\n"]

#print("".join(repr(line.encode()) + "\n" for line in lines))

barr = " ".join([x.split("\t")[1] for x in lines])
barrb = bytes.fromhex(barr.replace(" ", ""))

sys.stdout.buffer.write(barrb)