#!/bin/sh

export MINIO_ROOT_PASSWORD=$(cat "${MINIO_ROOT_PASSWORD_FILE}")
docker-entrypoint.sh
