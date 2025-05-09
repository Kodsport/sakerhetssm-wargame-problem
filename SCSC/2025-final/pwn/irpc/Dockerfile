FROM ubuntu:24.04@sha256:80dd3c3b9c6cecb9f1667e9290b3bc61b78c2678c02cbdae5f0fea92cc6734ab

RUN apt update && apt install -y gcc 

RUN mkdir /app
RUN useradd ctf

COPY irpc.c /app/irpc.c
COPY flag.txt /app/flag.txt
RUN gcc -fno-stack-protector -o /app/irpc /app/irpc.c

USER ctf

EXPOSE 1337

ENTRYPOINT while :; do /app/irpc 1337 ; sleep 5 ; done
