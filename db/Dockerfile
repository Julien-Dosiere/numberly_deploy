FROM postgres
COPY db-init.sql /docker-entrypoint-initdb.d/init.sql
ENV POSTGRES_USER numberly
ENV POSTGRES_PASSWORD numberly
ENV POSTGRES_DB numberly
EXPOSE 5732
