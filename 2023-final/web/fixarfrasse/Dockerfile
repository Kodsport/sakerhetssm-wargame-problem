FROM debian:bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    autoconf \
    bison \
    flex \
    g++ \
    gcc \
    git \
    iputils-ping \
    libnl-route-3-dev \
    libprotobuf-dev \
    libtool \
    make \
    php-cgi \
    php-sqlite3 \
    pkg-config \
    protobuf-compiler \
    python3 \
    python3-flask \
    python3-pip \
    openssl \
    python3-gunicorn \ 
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/web /var/web/certs
RUN openssl req -nodes -new -x509 -keyout /var/web/certs/server.cert.key -out /var/web/certs/server.cert \
    -subj "/DC=org/DC=OpenSSL/DC=users/UID=123456+CN=John Doe" # TODO: ???????

RUN sed -i 's/^disable_functions = .*/disable_functions = file_get_contents/' /etc/php/8.2/cgi/php.ini

RUN git clone https://github.com/google/nsjail.git /opt/nsjail
RUN cd /opt/nsjail && make && mv /opt/nsjail/nsjail /bin && rm -rf -- /opt/nsjail

COPY /src /app
WORKDIR /app

ENV FLASK_APP=server.py
ENV FLASK_ENV=production
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["python3", "-m", "gunicorn", "server:app", "-b :5000", "--certfile", "/var/web/certs/server.cert", "--keyfile", "/var/web/certs/server.cert.key"]
