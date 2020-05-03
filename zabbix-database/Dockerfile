FROM postgres

ENV POSTGRES_USER zabbix
COPY create.sql.gz /docker-entrypoint-initdb.d/create.sql.gz
