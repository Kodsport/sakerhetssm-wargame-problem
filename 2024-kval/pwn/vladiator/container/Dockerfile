FROM ubuntu:18.04

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

RUN apt-get update
RUN apt-get install -y python3 python3-pip xinetd binutils libssl-dev

ADD ctf.xinetd /etc/xinetd.d/ctf

COPY libc-2.27.so /lib/x86_64-linux-gnu/

COPY ELFSign /home/ctf/
COPY pubkey.pem /home/ctf/
COPY run.py /home/ctf/

COPY flag.txt /home/ctf/

RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/*

EXPOSE 1337

CMD ["/usr/sbin/xinetd", "-dontfork"]