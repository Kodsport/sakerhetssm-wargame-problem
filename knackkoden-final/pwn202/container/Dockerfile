FROM php:apache

RUN apt update -y && apt upgrade -y
RUN apt install python3 -y

COPY index.php /var/www/html/
COPY listig /var/www/html/
#COPY flag.py /var/www/html/
RUN chown -R root:root /var/www/html/
RUN chmod 4555 /usr/bin/python3
#RUN chmod 660 /var/www/html/flag.py
ENV FLAG SSM{En_Listig_Flagga}
