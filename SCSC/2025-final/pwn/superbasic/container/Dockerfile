FROM ubuntu:22.04 AS chroot

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y git make gcc

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

WORKDIR /home/ctf/
COPY flag.txt .
COPY main.c .

RUN git clone https://github.com/paladin-t/my_basic
RUN cp my_basic/core/* .
RUN gcc -o server my_basic.c main.c -lm -lrt

WORKDIR /

FROM ghcr.io/google/nsjail/nsjail:latest
COPY --from=chroot / /chroot

ENTRYPOINT nsjail --port 1337 --chroot /chroot/ --user 1337 --group 1337 --cwd /home/ctf/ \
  --tmpfsmount /tmp --bindmount_ro /etc/resolv.conf:/etc/resolv.conf -- /home/ctf/server
