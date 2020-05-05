FROM postgres

LABEL maintainer="tylerfrench2@gmail.com"

ENV POSTGRES_USER zabbix
COPY ./zabbix-database/zabbix-schema-5.sql.gz /docker-entrypoint-initdb.d/create.sql.gz