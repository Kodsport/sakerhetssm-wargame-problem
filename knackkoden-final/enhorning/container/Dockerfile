# Base image with PHP and Apache
FROM php:7.4-apache

# Install MariaDB server and PHP extensions
RUN apt-get update && apt-get install -y \
    mariadb-server \
    mariadb-client \
    && docker-php-ext-install mysqli

# Copy application files
COPY . /var/www/html/

# Copy and make the initialization script executable
COPY init.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/init.sh

# Expose port 80 for web traffic
EXPOSE 80

# Start MariaDB service and Apache server
CMD service mariadb start && /usr/local/bin/init.sh && apache2-foreground
