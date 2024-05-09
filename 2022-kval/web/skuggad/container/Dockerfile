FROM golang:1.16-alpine
RUN apk add build-base

WORKDIR /app
COPY . .
RUN go build -o /chall
EXPOSE 8080

CMD [ "/chall" ]