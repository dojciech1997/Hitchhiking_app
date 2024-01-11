#!/bin/bash

set -e

if [ ! "$(ls -A /var/lib/postgresql/data)" ]; then
    gosu postgres initdb
    gosu postgres pg_ctl -D /var/lib/postgresql/data -l /var/lib/postgresql/logfile start
    sleep 10
    gosu postgres psql -U postgres -d devops_db -f /docker-entrypoint-initdb.d/init.sql
    gosu postgres pg_ctl -D /var/lib/postgresql/data stop
fi

exec gosu postgres "$@"