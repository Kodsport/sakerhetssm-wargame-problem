FROM ubuntu:22.04 AS chroot

ARG DEBIAN_FRONTEND=noninteractive

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

RUN apt update -y
RUN apt install -y python3

WORKDIR /home/ctf/
COPY secrets.py .
COPY run_chall.sh .
COPY chall.py .

WORKDIR /

FROM ghcr.io/google/nsjail/nsjail:latest


COPY --from=chroot / /chroot

ENTRYPOINT nsjail --port 1337 --chroot /chroot/ --rw --user 1337 --group 1337 --cwd /home/ctf/ \
  --tmpfsmount /tmp --bindmount_ro /etc/resolv.conf:/etc/resolv.conf -- ./run_chall.sh
