FROM debian:bookworm-slim

ARG WEB_USER=webhost
ARG WEB_USER_UID=20000

RUN mkdir -p /var/www && \
    rm -rf /var/www/* && \
    useradd $WEB_USER \
        --uid $WEB_USER_UID \
        --user-group \
        --home-dir /var/www \
        --no-create-home \
        --password '!' && \
    chown -R $WEB_USER:$WEB_USER /var/www

# Install dependencies
RUN apt-get update && \
    apt-get install -y apache2 php php-curl php-xml p7zip-full composer \
        nodejs npm && \
    apt-get clean

# Create a directory for local testing
RUN mkdir -p /usr/local/share/webhosting

# Install dependencies for Node.js
USER $WEB_USER
WORKDIR /var/www
COPY --chown=$WEB_USER:$WEB_USER www/package.json .
RUN npm install

# Configure Apache
USER root
WORKDIR /etc/apache2
RUN mkdir -p sites-enabled && \
    a2enmod rewrite proxy
COPY apache2.conf .
COPY ./sites-enabled ./sites-enabled

ENV APACHE_RUN_DIR=/var/run/apache2
ENV APACHE_RUN_USER=$WEB_USER
ENV APACHE_RUN_GROUP=$WEB_USER
ENV APACHE_LOG_DIR=/var/log/apache2
ENV APACHE_PID_FILE=/var/run/apache2/httpd.pid

# Install dependencies for Laravel
USER $WEB_USER
WORKDIR /var/www
COPY --chown=$WEB_USER:$WEB_USER www .
RUN composer install && \
    ln -s $(pwd)/vendor/twbs/bootstrap-icons/bootstrap-icons.svg public/bootstrap-icons.svg
RUN npm run build

USER root
VOLUME /var/www/public/sites

COPY docker-entrypoint.sh /usr/local/bin
RUN chmod u=rwx,go=rx /usr/local/bin/docker-entrypoint.sh
CMD [ "/usr/local/bin/docker-entrypoint.sh" ]
