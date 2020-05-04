FROM postgres

LABEL maintainer="tylerfrench2@gmail.com"

ENV POSTGRES_USER zabbix
COPY zabbix-schema-5.sql /docker-entrypoint-initdb.d/create.sql
COPY zabbix-data-5.sql /docker-entrypoint-initdb.d/data.sql