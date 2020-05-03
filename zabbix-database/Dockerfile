FROM postgres

ENV POSTGRES_USER zabbix
COPY ./zabbix-database/create.sql.gz /docker-entrypoint-initdb.d/create.sql.gz
