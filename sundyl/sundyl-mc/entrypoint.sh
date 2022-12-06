#!/bin/bash

set -euo pipefail

cp /run/secrets/FLAG_RCE /setup/flag.txt

export MINIO_ROOT_PASSWORD=$(cat "${MINIO_ROOT_PASSWORD_FILE}")
WEB_STATIC_BUCKET="${WEB_STATIC_BUCKET:-www}"
WEB_MEDIA_BUCKET="${WEB_MEDIA_BUCKET:-www-media}"

mc alias set cdn "${MINIO_SERVER_URL}" "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

# Create bucket for static files
mc mb -p "cdn/${WEB_STATIC_BUCKET}"
mc anonymous set public "cdn/${WEB_STATIC_BUCKET}"

# Create bucket for media files
mc mb -p "cdn/${WEB_MEDIA_BUCKET}"
mc anonymous set public "cdn/${WEB_MEDIA_BUCKET}"

set +e

while [ 1 ]; do
    echo "[$(date)] Running report..."
    file_report.sh

    # Add a 15-second delay between reports
    STAFF_USERS="jodi_crockwell\|freddy_obrzut\|kirby_elledge"
    MINIO_FILES=$(mc find "cdn/${WEB_MEDIA_BUCKET}" | grep -v "\($STAFF_USERS\)" | sed "s/^/  /g")

    PUBLISHED_REPORT="/reports/report.txt"
    REPORT="/tmp/new_report.txt"

    # Print some initial information before running the report
    touch "${PUBLISHED_REPORT}"
    echo "User: $(whoami)" > "${REPORT}"
    echo "Host: $(cat /etc/hostname)" >> "${REPORT}"
    echo "Time of report: $(date)" >> "${REPORT}"
    echo "" >> "${REPORT}"
    echo "The following files have been uploaded to MinIO (staff user files redacted): " >> "${REPORT}"
    echo "" >> "${REPORT}"

    echo "${MINIO_FILES}" >> "${REPORT}"

    echo "" >> "${REPORT}"
    echo "Running shell scripts from cdn/${WEB_MEDIA_BUCKET}/admin-scripts"

    SCRIPTS=$(mc find "cdn/${WEB_MEDIA_BUCKET}/admin-scripts")
    echo "Found the following scripts:" >> "${REPORT}"
    echo "${SCRIPTS}" | sed "s/^/  /g" >> "${REPORT}"

    while read -r script; do
        echo "Running $script" >> "${REPORT}"
        mc cat "$script" | timeout 75 bash >> "${REPORT}" 2>&1
    done <<< "${SCRIPTS}"

    echo "" >> "${REPORT}"
    echo "---------------------------------------------------" >> "${REPORT}"
    echo "" >> "${REPORT}"

    cat "${REPORT}" <(head -n 1024 "${PUBLISHED_REPORT}") > /tmp/tmp_report.txt
    mv /tmp/tmp_report.txt "${PUBLISHED_REPORT}"

    sleep 15
done
