FROM mysql:8.0
ENV MYSQL_ROOT_PASSWORD root
COPY init.sql /mysql/
COPY after-init.sql /mysql/
COPY init.sh /docker-entrypoint-initdb.d/
COPY my.cnf /etc/mysql/
COPY entrypoint.sh /mysql/
ENTRYPOINT ["/mysql/entrypoint.sh"]