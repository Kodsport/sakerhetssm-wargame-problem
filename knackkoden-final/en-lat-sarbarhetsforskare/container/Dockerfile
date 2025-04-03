# Använd en Node.js-bild som bas
FROM node:14

# Sätt arbetskatalogen
WORKDIR /app

# Kopiera package-filer och installera beroenden
COPY package*.json ./
RUN npm install

# Kopiera resten av applikationen
COPY . .

# Exponera port 3000
EXPOSE 3000

# Startkommandot för applikationen
CMD ["node", "index.js"]
