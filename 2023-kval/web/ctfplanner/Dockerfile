FROM golang:1.19-alpine
RUN apk add build-base

WORKDIR /app
COPY . .
RUN go build -o /chall
EXPOSE 8080
ENV FLAG=SSM{du_bör_organisera_dina_homies_annars_homiar_organisationen_dig}

CMD [ "/chall" ]
