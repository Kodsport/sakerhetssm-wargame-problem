FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd python3

RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir -p /home/ctf/

COPY main.py /home/ctf/
COPY xinetd_config /etc/xinetd.d/

RUN chown -R root:ctf /home/ctf/
RUN chmod -R 750 /home/ctf/

CMD xinetd -dontfork
