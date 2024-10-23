from ubuntu:22.04 as chroot

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y strace
RUN apt install -y xinetd

RUN mkdir -p /home/ctf/

COPY xinetd_config /etc/xinetd.d/

COPY runner /home/ctf/
COPY run.sh /home/ctf/

EXPOSE 50000

CMD service xinetd restart && /bin/sleep infinity
