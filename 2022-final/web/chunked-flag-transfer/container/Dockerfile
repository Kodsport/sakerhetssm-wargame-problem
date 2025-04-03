FROM debian:bullseye

USER root
RUN apt-get update -y
RUN apt-get install -y openssl haproxy
RUN mkdir -p /var/web /var/web/certs
RUN openssl req -nodes -new -x509 -keyout /var/web/certs/server.cert.key -out /var/web/certs/server.cert \
    -subj "/DC=org/DC=OpenSSL/DC=users/UID=123456+CN=John Doe"

RUN apt-get install -y python3.9
COPY server.py http_parse.py /var/web/
COPY static /var/web/static

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
RUN touch /usr/local/etc/haproxy/net.log

COPY start.sh /start.sh


RUN chown -R haproxy /usr/local/etc/haproxy
RUN chown -R haproxy /var/web

CMD /bin/sh start.sh
