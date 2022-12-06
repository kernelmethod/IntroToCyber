#!/bin/bash

# Get a list of all of the names of files that have been uploaded
# to MinIO
FILES=$(mc find "cdn/${WEB_MEDIA_BUCKET}")

for file in $FILES; do
    bash -s << EOF

echo "[$(date)] Getting information on $file:"
mc stat $file

EOF
done
