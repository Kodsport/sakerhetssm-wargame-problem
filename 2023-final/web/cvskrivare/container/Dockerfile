FROM golang:1.20.3-bullseye
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y xz-utils && \
    mkdir /app && \
    cd /app && \
    wget https://github.com/typst/typst/releases/download/v0.3.0/typst-x86_64-unknown-linux-musl.tar.xz && \
    tar xvf typst-x86_64-unknown-linux-musl.tar.xz && \
    ln -sf /app/typst-x86_64-unknown-linux-musl/typst /bin/typst && \
    useradd user
WORKDIR /app
# cert.pem and key.pem generate with the following command:
# go run /usr/lib/go/src/crypto/tls/generate_cert.go --host 127.0.0.1
# generate_cert.go is also available here: https://github.com/golang/go/blob/master/src/crypto/tls/generate_cert.go
COPY default.png face.png gif.gif flag.txt index.html main.go mining.jpg cert.pem key.pem ./
# make it easy to find
COPY flag.txt flag
COPY flag.txt /flag.txt
COPY flag.txt /flag
RUN go build main.go && \
    chown user:user cert.pem key.pem
USER user
CMD ["./main"]
