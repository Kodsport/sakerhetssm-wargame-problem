FROM node:23-bookworm-slim

RUN apt update && apt install -y build-essential

WORKDIR /

COPY flag.txt /
RUN chmod 400 /flag.txt

COPY flagout.c /
RUN gcc flagout.c -o flagout && chmod 4111 flagout

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

WORKDIR /app

COPY package.json package-lock.json ./
COPY ./app/ ./app/

RUN npm ci
RUN npm run build

USER nextjs

EXPOSE 3000
ENV PORT=3000

ENV HOSTNAME="0.0.0.0"
CMD ["npm", "start"]
