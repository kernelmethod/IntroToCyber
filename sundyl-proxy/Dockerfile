FROM caddy:2-alpine

COPY entrypoint.sh /entrypoint.sh
RUN chmod u+rx,go-rwx /entrypoint.sh

COPY Caddyfile /etc/caddy/Caddyfile
COPY www /usr/share/caddy

CMD [ "/entrypoint.sh" ]
