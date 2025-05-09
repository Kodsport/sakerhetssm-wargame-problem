FROM node:current-alpine3.21
WORKDIR /app
RUN apk add --no-cache \
    bash build-base \
    && rm -rf /var/cache/apk/*

COPY package*.json ./
RUN npm ci --only=production
COPY app.js ./
COPY run.sh /
RUN chmod +x /run.sh
COPY ./public /app/public

COPY flag.txt /
RUN chmod 400 /flag.txt
COPY flagout.c /
RUN cd /; gcc flagout.c -o flagout && chmod 4111 flagout

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser
EXPOSE 3000

CMD ["/run.sh"]