#!/bin/sh

set -eux

# Substitute IP address into the record files that end in _template
export IPV4_ADDR="${IPV4_ADDR:-127.0.0.1}"
find /etc/namedb/template -type f | \
    xargs -I{} sh -c 'sed -e 's/IPV4_ADDR/$IPV4_ADDR/g' {} > /etc/zones/$(basename {})'

# Copy remaining record files
find /etc/namedb -type f -maxdepth 1 | \
    xargs -I{} sh -c 'cp {} /etc/zones/$(basename {})'

/usr/sbin/named -g $OPTIONS
