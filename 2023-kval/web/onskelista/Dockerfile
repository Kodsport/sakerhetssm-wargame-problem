# ---- build stage ----
FROM golang:1.22-bookworm AS gobuild
COPY main.go go.mod go.sum /src/
COPY static/ /src/static/
WORKDIR /src
RUN go build -o /x

# ---- runtime stage ----
FROM node:18-bookworm

# Add Google Chrome repo using keyring (no apt-key)
RUN apt-get update \
 && apt-get install -y --no-install-recommends wget gnupg ca-certificates \
 && install -m 0755 -d /etc/apt/keyrings \
 && wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /etc/apt/keyrings/google-linux-signing-keyring.gpg \
 && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux-signing-keyring.gpg] https://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
      google-chrome-stable \
      fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont libxss1 \
 && rm -rf /var/lib/apt/lists/*

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

COPY --from=gobuild /x /x

WORKDIR /usr/src/app
COPY ./ ./
RUN npm install

RUN groupadd -r pptruser && useradd -r -g pptruser -G audio,video pptruser \
 && chown -R pptruser:pptruser node_modules

USER pptruser
EXPOSE 8080
ENTRYPOINT ["/x"]
