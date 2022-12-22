#!/bin/bash

set -euo pipefail

PASSWORDS="$1"
cryptfile=$(mktemp -u)

for passfile in $(find "$PASSWORDS" -type f); do
    username=$(basename "$passfile")
    mkpasswd -sm yescrypt < "$passfile" > "$cryptfile"

    useradd "$username" \
        --create-home \
        --password $(cat "$cryptfile") \
        --groups ssh-access,lab-users \
        --user-group \
        --shell /bin/bash
done

rm -f "$cryptfile"
