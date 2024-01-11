# database/Dockerfile
FROM postgres:latest

ENV POSTGRES_DB devops_db
ENV POSTGRES_USER wojtek
ENV POSTGRES_PASSWORD password

VOLUME /docker-entrypoint-initdb.d/

COPY ./postgresql.conf /etc/postgresql/postgresql.conf
COPY ./entrypoint.sh /usr/local/bin/

# Opcjonalne: Ustawienie specyficznych opcji konfiguracji PostgreSQL (jeśli potrzebne)
# ENV POSTGRES_CONFIG_OPTION=value
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]

CMD ["postgres"]

EXPOSE 5432