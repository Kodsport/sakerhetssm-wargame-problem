import subprocess

output = subprocess.check_output('strings -t x -e l chall.dmp | grep -i flag', shell=True).split()[0]
addr = int(output.decode(), 16)
f = open('chall.dmp', 'rb').read()

end = 0
for i, b in enumerate(f, addr):
    if b == 0 and f[i - 1] == ord('}'):
        end = i
        break
print(f[addr:end + 1].decode('utf-16-le'))
