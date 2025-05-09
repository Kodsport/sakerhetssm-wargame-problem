FROM php:apache

RUN apt update -y && apt upgrade -y
RUN apt install python3 -y

COPY index.php /var/www/html/
COPY getflag /var/www/html/
RUN chown -R root:root /var/www/html/
RUN chmod +x /var/www/html/getflag
