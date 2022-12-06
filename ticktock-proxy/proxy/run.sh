#!/bin/sh

set -eux

echo "${NGINX_ADDTL_CONFD}" | \
    tr ',' '\n' | \
    xargs -I '{}' echo "include /etc/nginx/conf.d/{};" \
    > /etc/nginx/snippets/include.conf

# Substitute environment variables into config files
export DOLLAR='$'
envsubst < /etc/nginx/snippets/proxy.template.conf \
    > /etc/nginx/snippets/proxy.conf

chmod a+r /etc/nginx/snippets/include.conf
nginx -g 'daemon off;'
