FROM python:latest AS builder

WORKDIR /build
COPY src /build/src
COPY Makefile /build
RUN make build

FROM nginx:latest

COPY --from=builder /build/build/index.html /usr/share/nginx/html/index.html
COPY --from=builder /build/build/congratulations.js /usr/share/nginx/html/congratulations.js
COPY --from=builder /build/build/999999th-visitor-you-won.gif /usr/share/nginx/html/999999th-visitor-you-won.gif
