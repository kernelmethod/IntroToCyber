FROM caddy:2-alpine

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod a+rx,go-w /usr/local/bin/docker-entrypoint.sh

COPY Caddyfile /etc/caddy/Caddyfile

CMD [ "docker-entrypoint.sh" ]
