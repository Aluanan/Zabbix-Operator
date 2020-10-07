#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE USER zbx_monitor WITH PASSWORD 'zabbix';
GRANT SELECT ON pg_stat_database TO zbx_monitor;
ALTER USER zbx_monitor WITH SUPERUSER;
EOSQL