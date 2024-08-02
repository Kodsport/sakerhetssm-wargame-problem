FROM golang:1.22.1

RUN mkdir /app
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download
RUN curl -L -o pkl 'https://github.com/apple/pkl/releases/download/0.26.2/pkl-linux-amd64' && chmod +x pkl && mv pkl /usr/local/bin/pkl

COPY main.go base.pkl ./
COPY html ./html

RUN go build -o /app/main .

RUN useradd -ms /bin/bash user
RUN chmod -R  +rx /app
USER user

EXPOSE 5000
ENV FLAG=SSM{s4nit1z3_y0ur_pkl_1nputs}

CMD ["/app/main"]
