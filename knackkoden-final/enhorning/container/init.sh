#!/bin/bash

# Wait for MariaDB to start
sleep 5

# Secure the installation by setting a root password and creating the database
mysql -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('password'); FLUSH PRIVILEGES;"
mysql -uroot -ppassword -e "CREATE DATABASE IF NOT EXISTS unicorn_magic;"

# Populate the database with the initial data
mysql -uroot -ppassword unicorn_magic <<EOF
CREATE TABLE IF NOT EXISTS unicorns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    color VARCHAR(50),
    power VARCHAR(100)
);

INSERT INTO unicorns (name, color, power) VALUES
('Starlight', 'Sparkling Silver', 'Rainbow Generation'),
('Moonbeam', 'Glowing Purple', 'Night Vision'),
('Sunshine', 'Golden Yellow', 'Solar Flare Control'),
('FlagUnicorn', 'Invisible', 'SSM{en_glittrande_magisk_tabell}');
EOF
