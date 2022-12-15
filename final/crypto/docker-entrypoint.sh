#!/bin/sh

set -euo pipefail

uvicorn \
    --port 8000 \
    --host 0.0.0.0 \
    cryptoapi.main:app
