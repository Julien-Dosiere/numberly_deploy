FROM postgres
COPY ./db-init.sql /docker-entrypoint-initdb.d/init.sql
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres
EXPOSE 5432
