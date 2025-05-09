#!/bin/bash
cd "/app";
while true; do
    find /tmp -type f -mmin +60 -delete 2>/dev/null;
    if [ -z "$(pidof node)" ]; then
        echo "node died for some reason, restarting...";
        bash -c 'npm start &';
    fi
    sleep 300;
done;