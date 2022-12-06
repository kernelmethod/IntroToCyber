FROM alpine:3.16

RUN apk add --no-cache bind bind-tools

# Create directories for bind
RUN \
    mkdir -p /var/cache/named && \
    mkdir -p /var/log/named && \
    mkdir -p /etc/bind/conf.d && \
    mkdir -p /etc/namedb /etc/zones && \
    chown -R named:named /var/cache/named /var/log/named && \
    chown -R named:named /etc/zones && \
    chown -R root:named /etc/namedb && \
    chmod -R g+r,g-w /etc/namedb

WORKDIR /etc/bind
COPY --chown=named:named entrypoint.sh /
RUN chmod u+x /entrypoint.sh

COPY --chown=root:named named.conf /etc/bind/named.conf
COPY --chown=root:named conf /etc/bind/conf.d
COPY --chown=root:named namedb /etc/namedb

# Fix permissions on config files
RUN chown -R root:named /etc/bind && \
    chmod -R g+rw /etc/bind

CMD [ "/entrypoint.sh" ]
