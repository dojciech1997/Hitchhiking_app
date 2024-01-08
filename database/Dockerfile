# database/Dockerfile
FROM postgres:latest

COPY ./database/init.sql /docker-entrypoint-initdb.d/

COPY ./database/postgresql.conf /etc/postgresql/postgresql.conf

# Opcjonalne: Ustawienie specyficznych opcji konfiguracji PostgreSQL (jeśli potrzebne)
# ENV POSTGRES_CONFIG_OPTION=value

EXPOSE 5432