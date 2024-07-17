FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y

RUN apt install -y python3 python3-pip nginx wget
RUN pip3 install flask gunicorn pymongo
RUN apt-get install -y gnupg curl

RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt update
RUN apt install mongodb-org -y

RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir -p /home/ctf/

COPY ctf-site /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default
COPY flag.txt setup.py setup.sh start.sh /home/ctf/

RUN chown -R root:ctf /home/ctf/
RUN chmod -R 750 /home/ctf/

WORKDIR /home/ctf/

RUN mkdir /data
RUN mkdir /data/db
RUN /home/ctf/setup.sh

COPY templates /home/ctf/templates/
COPY server.py /home/ctf/
CMD /home/ctf/start.sh
