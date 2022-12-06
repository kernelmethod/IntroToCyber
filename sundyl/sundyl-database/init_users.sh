#!/bin/sh

set -e

# Setup users for the database
POSTGRES_WEB_PASSWORD=$(cat "${POSTGRES_WEB_PASSWORD_FILE}")

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<- EOF

CREATE USER admin WITH PASSWORD '${POSTGRES_WEB_PASSWORD}';
CREATE DATABASE webdata;
GRANT ALL PRIVILEGES ON DATABASE webdata TO admin;

EOF
