from ubuntu:22.04

# Install the necessary packages
RUN apt-get update && apt-get install -y \
    gcc-aarch64-linux-gnu \
    qemu-user


RUN mkdir /serve
WORKDIR /serve
COPY web_serve /serve/.
RUN chmod +x /serve/web_serve
COPY parse /serve/parse
RUN chmod +x /serve/parse

ENV QEMU_LD_PREFIX="/usr/aarch64-linux-gnu/"

# Set the entrypoint
ENTRYPOINT ["/serve/web_serve"]
