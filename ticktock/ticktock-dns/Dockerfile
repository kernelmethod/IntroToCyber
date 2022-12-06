FROM alpine:3.16

RUN apk add --no-cache bind bind-tools

# Create directories for bind
RUN \
    mkdir -p /var/named && \
    mkdir -p /var/cache/named && \
    mkdir -p /var/log/named && \
    mkdir -p /etc/bind/conf.d && \
    mkdir -p /etc/namedb /etc/zones && \
    chown -R named:named /var/named /var/cache/named /var/log/named && \
    chown -R named:named /etc/zones && \
    chown -R root:named /etc/namedb && \
    chmod -R g+r,g-w /etc/namedb

COPY --chown=named:named entrypoint.sh /
RUN chmod u+x /entrypoint.sh

COPY --chown=root:named named.conf /etc/bind/named.conf
COPY --chown=root:named conf /etc/bind/conf.d
COPY --chown=root:named db /etc/namedb

# Fix permissions on config files
RUN chown -R root:named /etc/bind && \
    chmod -R g-w,g+r /etc/bind

# Run the server as named
USER named

WORKDIR /etc/bind

VOLUME /etc/bind/conf.d /etc/namedb
EXPOSE 53/tcp 53/udp

CMD [ "/entrypoint.sh" ]
