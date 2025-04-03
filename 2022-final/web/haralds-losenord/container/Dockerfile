FROM php:apache

COPY index.php /var/www/html/
COPY source.php /var/www/html/
COPY sauce.png /var/www/html/
RUN chown -R root:root /var/www/html/

COPY 000-default.conf /etc/apache2/sites-available
COPY certs/cert.crt /etc/ssl/certs/cert.crt
COPY certs/private.key /etc/ssl/private/private.key
RUN a2enmod ssl && a2enmod rewrite #&& a2enmod socache_shmcb
RUN service apache2 restart

COPY flag.txt /
RUN chown root:root /flag.txt
RUN chmod 644 /flag.txt
