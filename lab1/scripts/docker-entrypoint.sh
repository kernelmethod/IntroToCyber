#!/bin/sh

set -eux

mkdir -p /run/sshd
exec /usr/sbin/sshd -D
