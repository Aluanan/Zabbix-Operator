FROM postgres

LABEL maintainer="tylerfrench2@gmail.com"

ENV POSTGRES_USER zabbix
COPY zabbix-create-5.sql /docker-entrypoint-initdb.d/create.sql