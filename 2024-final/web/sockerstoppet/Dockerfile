FROM golang:1.22.2-bookworm

COPY ./container /app

WORKDIR /app
RUN go build -o server main.go

ENV FLAG=SSM{mmm_grädde_so_good_yum_yum}

ENTRYPOINT /app/server