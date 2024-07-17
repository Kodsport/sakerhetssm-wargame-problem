#!/bin/bash
mongod &
nginx
gunicorn server -b 0.0.0.0:8000 -u ctf -g ctf