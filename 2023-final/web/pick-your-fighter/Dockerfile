FROM golang:1.19-alpine
#RUN apk add build-base

WORKDIR /app
COPY src/ .
RUN go build -o /chall
EXPOSE 8443

CMD [ "/chall" ]
