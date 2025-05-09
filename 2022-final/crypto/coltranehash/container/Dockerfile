FROM ubuntu:20.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-flask gunicorn nginx

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

COPY server.py index.html logged_in.html secrets.txt /home/ctf/
COPY nginx.conf /etc/nginx/nginx.conf
COPY certs/ /var/web/certs

RUN chown -R root:ctf /home/ctf/
RUN chmod -R 750 /home/ctf/

WORKDIR /home/ctf/

CMD nginx && gunicorn server:app -b unix:/tmp/ctf.sock -u ctf -g ctf
