# ====== PostgreSQL EHR ======
FROM postgres:17

# Copia schema EHR
COPY init.sql /docker-entrypoint-initdb.d/

# Variabili di default (modificabili in K8s)
ENV POSTGRES_DB=ehr
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=secret

EXPOSE 5432
