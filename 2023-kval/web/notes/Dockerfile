FROM golang:1.19-alpine
RUN apk add build-base

WORKDIR /app
COPY . .
RUN go build -o /chall
EXPOSE 8080
ENV FLAG=SSM{c17r0n_d1j0n53n4p_011v01j4_t1ll_53113r1}

CMD [ "/chall" ]
