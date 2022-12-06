#!/bin/sh

set -euxo pipefail

S3_MOUNT=/s3/gallery
export RCLONE_CONFIG=$(mktemp)
chmod go-rwx "${RCLONE_CONFIG}"

cat << EOF >> ${RCLONE_CONFIG}
[minio]
type = s3
provider = Minio
env_auth = false
access_key_id = ${MINIO_ROOT_USER}
secret_access_key = ${MINIO_ROOT_PASSWORD}
endpoint = http://s3.ticktock.lab:9000
location_constraint = 
server_side_encryption =
EOF

echo "Wrote rclone config to ${RCLONE_CONFIG}"

# Unmount the directory if it is currently mounted
mountpoint -q "${S3_MOUNT}" && fusermount -u "${S3_MOUNT}"

# mkdir may fail if the directory is still mounted
mkdir -p "${S3_MOUNT}" || fusermount -u "${S3_MOUNT}"

# Intentionally small cache time / poll interval to ensure that we see
# changes to the buckets as soon as they're available.
rclone mount minio:gallery "${S3_MOUNT}" \
    --allow-other \
    --dir-cache-time=5s \
    --poll-interval=5s \
    --verbose=3 \
    --read-only
