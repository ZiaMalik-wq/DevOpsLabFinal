FROM postgres:15-alpine

# Environment variables for default initialization
# (These can be overridden by docker-compose, but we set some defaults)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=skillgap_db

# (Optional) You can copy initialization scripts if you have them:
# COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
