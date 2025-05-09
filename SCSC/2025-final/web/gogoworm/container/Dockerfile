FROM golang:1.24.1-bookworm

COPY [^Docker]* /app/

WORKDIR /app
RUN go build -o server main.go

ENV FLAG=SNHT{vår_och_höst}

ENTRYPOINT /app/server