FROM ubuntu:22.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-numpy

RUN mkdir /chall
COPY server.py /chall/
COPY wavs /chall/wavs
WORKDIR /chall

CMD python3 server.py