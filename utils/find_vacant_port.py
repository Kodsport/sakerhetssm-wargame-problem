import os
import yaml
import sys

START_PORT = 40000
END_PORT = 50000
LIMIT = 5
VERBOSE = False

if len(sys.argv) > 1:
    START_PORT = int(sys.argv[1])  # Arg1: Start port
if len(sys.argv) > 2:
    END_PORT = int(sys.argv[2])  # Arg2: End port
if len(sys.argv) > 3:
    LIMIT = int(sys.argv[3])  # Arg3: Limit
if len(sys.argv) > 4:
    VERBOSE = bool(sys.argv[4])  # Arg4: Verbose

start = "."
max_back = 10

while "ctf.yml" not in os.listdir(start):
    start += "/.."
    max_back -= 1
    if max_back == 0:
        print("ctf.yml not found")
        exit(1)


taken_ports = []

for r in os.walk(start):
    for name in ["challenge.yml", "challenge.yaml"]:
        if name in r[2]:
            with open(r[0] + f"/{name}", "rt", encoding="utf8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if "service" in data and "external_port" in data["service"]:
                    taken_ports.append(data["service"]["external_port"])

taken_ports.sort()
printed = 0
free_ports = []

if VERBOSE:
    print("Taken ports:")
    print(taken_ports)

for i in range(START_PORT, END_PORT):
    if i not in taken_ports:
        free_ports.append(i)
        printed += 1
        if printed == LIMIT:
            break

print(f"Searching for {LIMIT} free ports between {START_PORT} and {END_PORT}")
print("Available ports:")
print(free_ports)
