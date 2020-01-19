FROM php:7.3-fpm
RUN docker-php-ext-install pdo pdo_mysql
COPY www.conf /usr/local/etc/php-fpm.d/
COPY php.ini /usr/local/etc/php/conf.d/
CMD ["php-fpm", "--allow-to-run-as-root"]