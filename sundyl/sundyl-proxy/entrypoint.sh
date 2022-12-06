#!/bin/sh

set -euo pipefail

# Set environment variables from secrets
if [ -f /run/secrets/FLAG_WILDCARD_SUBDOMAIN ]; then
    export FLAG_WILDCARD_SUBDOMAIN=$(cat /run/secrets/FLAG_WILDCARD_SUBDOMAIN)
else
    export FLAG_WILDCARD_SUBDOMAIN="flag{wildcard:000000}"
fi

if [ -f /run/secrets/FLAG_WILDCARD_PORT_ENUMERATION ]; then
    export FLAG_WILDCARD_PORT_ENUMERATION=$(cat /run/secrets/FLAG_WILDCARD_PORT_ENUMERATION)
else
    export FLAG_WILDCARD_PORT_ENUMERATION="flag{wildcard:000000}"
fi

if [ -f /run/secrets/SECRET_SUBDOMAIN ]; then
    export SECRET_SUBDOMAIN=$(cat /run/secrets/SECRET_SUBDOMAIN)
else
    export SECRET_SUBDOMAIN="secret"
fi

if [ -f /run/secrets/SECRET_PORT ]; then
    export SECRET_PORT=$(cat /run/secrets/SECRET_PORT)
else
    export SECRET_PORT="57230"
fi

# Start proxy server
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
