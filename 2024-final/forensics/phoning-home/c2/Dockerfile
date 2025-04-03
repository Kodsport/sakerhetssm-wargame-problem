FROM debian:bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3

RUN mkdir -p /app
WORKDIR /app
COPY server.py malware.py ./

ENTRYPOINT ["python3", "-u", "server.py", "0.0.0.0", "80", "5000"]
