FROM debian:bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y tcpdump

ENTRYPOINT ["tcpdump", "-i", "eth0", "-n", "-w", "/data/capture.pcap"]
