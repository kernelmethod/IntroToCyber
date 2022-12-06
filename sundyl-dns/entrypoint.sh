#!/bin/sh

set -eux

export BASE_DOMAIN="${BASE_DOMAIN:-example.org}"
export IPV4_ADDR="${IPV4_ADDR:-127.0.0.1}"

if [ "${VCR:-0}" -eq 1 ]; then
    export IPV4_ADDR=$(nslookup terminal.example.com -type=a | grep -v 127.0.0 | awk '/Address: / { print $2; }')
fi

varsubst() {
    echo "Substituting variables into $1" >&2
    sed -e "s/IPV4_ADDR/$IPV4_ADDR/g" \
        -e "s/BASE_DOMAIN/$BASE_DOMAIN/g" \
        "$1"
}

setperms() {
    chown root:named "$1"
    chmod g+r "$1"
}

# Substitute variables in named.conf
OUTFILE=$(mktemp)
varsubst /etc/bind/conf.d/named.conf > "${OUTFILE}"
mv "${OUTFILE}" /etc/bind/conf.d/named.conf
setperms /etc/bind/conf.d/named.conf

# Substitute variables into zone template file
varsubst /etc/namedb/db.template > "/etc/zones/db.${BASE_DOMAIN}"
setperms "/etc/zones/db.${BASE_DOMAIN}"

# Copy remaining record files
cp /etc/namedb/localhost.rev /etc/zones/localhost.rev
setperms /etc/zones/localhost.rev

/usr/sbin/named -g -u named
