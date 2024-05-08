FROM node

WORKDIR /app
COPY . /app

RUN apt update
RUN apt install php-common php-cli php-sqlite3 -y
RUN npm install express

RUN mkdir /app/data
RUN chown -R www-data:www-data /app/data

USER www-data
RUN php -f init.php

CMD [ "node", "index.js" ]