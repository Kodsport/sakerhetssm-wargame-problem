import os
import yaml
import sys

START_PORT = 40000
END_PORT = 50000
LIMIT = 5
VERBOSE = False

# You do not need to run this with args :)
if len(sys.argv) > 1:
    START_PORT = int(sys.argv[1])
if len(sys.argv) > 2:
    END_PORT = int(sys.argv[2])
if len(sys.argv) > 3:
    LIMIT = int(sys.argv[3])
if len(sys.argv) > 4:
    VERBOSE = bool(sys.argv[4])

start = "."
max_back = 10

# Find the root of the repository
while "README.md" not in os.listdir(start):
    start += "/.."
    max_back -= 1
    if max_back == 0:
        print(
            "README.md not found. Make sure README.md is in the root of this repository"
        )
        exit(1)


taken_ports = []
used_challenge_ids = []


def check_port(port, name):
    if port < START_PORT or port >= END_PORT:
        print(f"Port {port} is outside of the range {START_PORT}-{END_PORT} in {name}")


def add_challenge_id(challenge_id, name):
    if challenge_id in used_challenge_ids:
        print(f"Challenge ID {challenge_id} is already in use in {name}")
    used_challenge_ids.append(challenge_id)


# Find all currently taken ports
for r in os.walk(start):
    for name in ["challenge.yml", "challenge.yaml"]:
        if name in r[2]:
            with open(r[0] + f"/{name}", "rt", encoding="utf8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if "challenge_id" in data:
                    add_challenge_id(data["challenge_id"], r[0])
                if "service" in data and "external_port" in data["service"]:
                    taken_ports.append(data["service"]["external_port"])
                    check_port(data["service"]["external_port"], r[0])
                if "deployment" in data and "containers" in data["deployment"]:
                    if "containers" in data["deployment"]:
                        for container in data["deployment"]["containers"].values():
                            if "services" in container:
                                for service in container["services"]:
                                    if "external_port" in service:
                                        taken_ports.append(service["external_port"])
                                        check_port(service["external_port"], r[0])
                            if "extra_exposed_ports" in container:
                                for ports in container["extra_exposed_ports"]:
                                    if "external_port" in ports:
                                        taken_ports.append(ports["external_port"])
                                        check_port(ports["external_port"], r[0])

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
