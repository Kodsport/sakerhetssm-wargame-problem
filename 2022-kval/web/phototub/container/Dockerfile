FROM php:apache

COPY flag.txt /
COPY index.php phototub.jpg /var/www/html/
RUN mkdir /var/www/html/uploads
RUN chmod 773 /var/www/html/uploads
RUN chown -R root:root /var/www/html/
