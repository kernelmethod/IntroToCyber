#!/bin/sh

cp /run/secrets/FLAG_WILDCARD_SOURCE_CONTROL www/flag.txt
fossil add ./www/flag.txt
fossil commit -m "Add source control flag"

lighttpd -D -f /etc/lighttpd/lighttpd.conf
