# Setting up chroot below
FROM ubuntu:18.04 AS chroot

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

COPY ropabara /home/ctf/
COPY flag.txt /home/ctf/

# Now setting up the actual container
FROM ghcr.io/google/nsjail/nsjail:latest

USER root
RUN echo "deb [trusted=yes] http://deb.debian.org/debian bullseye main\ndeb [trusted=yes] http://security.debian.org/debian-security bullseye-security main\ndeb [trusted=yes] http://deb.debian.org/debian bullseye-updates main" >> /etc/apt/sources.list

RUN apt-get update -y
RUN apt-get install -y openssl haproxy
RUN mkdir -p /var/web /var/web/certs
RUN openssl req -nodes -new -x509 -keyout /var/web/certs/server.cert.key -out /var/web/certs/server.cert \
    -subj "/DC=org/DC=OpenSSL/DC=users/UID=123456+CN=John Doe"

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
RUN touch /usr/local/etc/haproxy/net.log

COPY --from=chroot / /chroot

CMD haproxy -D -f /usr/local/etc/haproxy/haproxy.cfg & nsjail --port 1337 --chroot /chroot/ --user 1337 --group 1337 --cwd /home/ctf/ --tmpfsmount /tmp --bindmount_ro /etc/resolv.conf:/etc/resolv.conf /home/ctf/ropabara