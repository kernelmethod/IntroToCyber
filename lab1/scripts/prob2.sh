#!/bin/bash
# Setup script for Problem 2

set -euo pipefail

PASSWORD="$1"
TEMPLATE="XXXXXXXXXX"

mkdir -p ./problem
seq 1 1024 | \
    xargs -I'{}' mktemp -dp ./problem "$TEMPLATE"

SOLUTION_DIR=$(find ./problem -mindepth 1 -type d | shuf -n1)
echo "$PASSWORD" > "$SOLUTION_DIR/password.txt"
