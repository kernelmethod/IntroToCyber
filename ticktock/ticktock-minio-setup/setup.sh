#!/bin/sh

set -exuo pipefail

mc alias set ticktock "http://${MINIO_HOST}:9000" "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

mc mb -p "ticktock/${MINIO_BUCKET_AVATARS}"
mc anonymous set public "ticktock/${MINIO_BUCKET_AVATARS}"

mc mb -p "ticktock/${MINIO_BUCKET_GALLERY}"

# Mirror the contents of the gallery folder to the corresponding bucket
mc mirror ./gallery "ticktock/${MINIO_BUCKET_GALLERY}"

exit 0
