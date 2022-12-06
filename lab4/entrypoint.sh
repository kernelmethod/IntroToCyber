#!/bin/bash

set -euo pipefail

unshadow /etc/passwd /etc/shadow | \
    grep -E "^(${SPEED_USER_PREFIX}|${PWCRACK_USER_PREFIX})"
