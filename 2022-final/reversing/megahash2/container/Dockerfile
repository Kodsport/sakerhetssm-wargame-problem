FROM nginx
COPY html /usr/share/nginx/html

COPY default.conf /etc/nginx/conf.d/default.conf
COPY certs/private.key /etc/ssl/private
COPY certs/cert.crt  /etc/ssl/certs
