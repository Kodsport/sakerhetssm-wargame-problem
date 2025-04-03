#!/bin/sh

docker buildx build -t ssm_alldelesvanligpython .
docker run --rm -it ssm_alldelesvanligpython:latest
