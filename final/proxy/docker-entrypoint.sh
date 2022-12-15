#!/bin/sh

set -euo pipefail

caddy run \
    --config /etc/caddy/Caddyfile \
    --adapter caddyfile
