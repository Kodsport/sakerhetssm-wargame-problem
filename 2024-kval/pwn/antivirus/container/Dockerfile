FROM ubuntu:20.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-flask gunicorn nginx

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/
RUN mkdir -p /home/ctf/uploads

COPY av.py /home/ctf/
COPY av /home/ctf/
COPY nginx.conf /etc/nginx/nginx.conf
COPY flag /flag

RUN chown -R root:ctf /home/ctf/
RUN chown -R ctf:ctf /home/ctf/uploads
RUN chmod -R 750 /home/ctf/
RUN chmod 744 /flag

WORKDIR /home/ctf/

CMD nginx && gunicorn av:app -b unix:/tmp/ctf.sock -u ctf -g ctf
