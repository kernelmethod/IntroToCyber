#!/bin/bash

umask 0077
set -euo pipefail

PASSWORDS="$1"
PASSWORDS_OUTDIR="$2"

mkdir -p "$PASSWORDS_OUTDIR"

cryptfile=$(mktemp -u)

while read line; do
    username=$(echo "$line" | cut -d: -f1)
    password=$(echo "$line" | cut -d: -f2)
    echo "$password" > "$PASSWORDS_OUTDIR/$username"
    mkpasswd -sm yescrypt <"$PASSWORDS_OUTDIR/$username" > "$cryptfile"

    useradd "$username" \
        --create-home \
        --password $(cat "$cryptfile") \
        --groups ssh-access,lab-users \
        --user-group \
        --shell /bin/bash

    chown root "/home/$username"
done < "$PASSWORDS"

rm -f "$cryptfile"
