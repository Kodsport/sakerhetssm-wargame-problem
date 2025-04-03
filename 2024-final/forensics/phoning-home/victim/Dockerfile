FROM debian:bookworm-slim as chrome

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y curl
RUN curl -o /etc/apt/trusted.gpg.d/google.asc https://dl.google.com/linux/linux_signing_key.pub

FROM debian:bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive

COPY --from=chrome /etc/apt/trusted.gpg.d/google.asc /etc/apt/trusted.gpg.d/google.asc
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y \
    # Python
    python3 python3-pip python3-venv \
    # Google Chrome
    google-chrome-stable

RUN mkdir -p /app
WORKDIR /app
RUN python3 -m venv env
COPY requirements.txt .
RUN env/bin/pip install -r requirements.txt
COPY cache.py driver.py ./
RUN env/bin/python3 -u cache.py

ENTRYPOINT ["env/bin/python3", "-u", "driver.py", "SSM{apt_ph0ne_h0m3}"]
