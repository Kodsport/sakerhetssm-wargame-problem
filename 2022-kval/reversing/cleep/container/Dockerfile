# Setting up chroot below
FROM ubuntu:20.04 AS chroot

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

RUN apt-get update && apt-get install -y netcat-traditional python3

COPY service /home/ctf/
RUN chown -R 1337:1337 /home/ctf

USER 1337

ENTRYPOINT while true; do cd /home/ctf; python3 service; done

