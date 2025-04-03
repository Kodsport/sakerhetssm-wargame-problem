# Setting up chroot below
FROM ubuntu:20.04 AS chroot

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

RUN apt-get update && apt-get install -y python3

COPY exec exec.c build.py flag.txt /home/ctf/

WORKDIR /home/ctf

RUN chown 256:256 flag.txt && \
chmod 400 flag.txt && \
python3 build.py && \
rm build.py && \
rm exec

# Now setting up the actual container
FROM ghcr.io/google/nsjail/nsjail:latest

COPY --from=chroot / /chroot

ENTRYPOINT nsjail --port 1337 --chroot /chroot/ --user 1337:0:65535 --group 1337:0:65535 --cwd /home/ctf/ --tmpfsmount /tmp --bindmount_ro /etc/resolv.conf:/etc/resolv.conf --disable_no_new_privs /bin/sh
