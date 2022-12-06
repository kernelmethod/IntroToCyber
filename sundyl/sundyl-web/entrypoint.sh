#!/bin/sh

set -eux

export FLAG_CSRF=$(cat "/run/secrets/FLAG_CSRF")
export FLAG_XSS=$(cat "/run/secrets/FLAG_XSS")
export MINIO_ROOT_PASSWORD=$(cat "${MINIO_ROOT_PASSWORD_FILE}")

# Perform database migrations
python3 manage.py migrate

# Send static files to S3
python3 manage.py collectstatic --noinput -v 1

# Perform app setup
python3 manage.py setup_app

# Run gunicorn sever
gunicorn -c /usr/share/gunicorn/gunicorn.conf.py sundyl.wsgi
