#/bin/sh
haproxy -D -f /usr/local/etc/haproxy/haproxy.cfg

echo haproxy started

cd /var/web
while [ true ]
do
    python3.9 server.py
done
