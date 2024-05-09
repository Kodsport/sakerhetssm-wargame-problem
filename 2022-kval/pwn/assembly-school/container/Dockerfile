# Setting up chroot below
FROM ubuntu:20.04 AS chroot

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3 binutils

COPY service /home/ctf/

# Now setting up the actual container
FROM ghcr.io/google/nsjail/nsjail:latest

COPY --from=chroot / /chroot

ENTRYPOINT nsjail --port 1337 --chroot /chroot/ --user 1337 --group 1337 --cwd /home/ctf/ --tmpfsmount /tmp --bindmount_ro /etc/resolv.conf:/etc/resolv.conf /home/ctf/service
