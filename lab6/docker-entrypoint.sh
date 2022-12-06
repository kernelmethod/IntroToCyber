#!/bin/bash

set -euo pipefail

VITE_DEV="${VITE_DEV:-0}"
rm -f "${APACHE_PID_FILE}"

# Generate encryption key
php artisan key:generate

if [[ -z "${VITE_DEV}" ]] || [[ "${VITE_DEV}" -eq 0 ]]; then
    npm run build
else
    npm run dev -- --host &
fi

apache2 -DFOREGROUND
