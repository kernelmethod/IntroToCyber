FROM php:7.2-apache

WORKDIR /var/www/html

# Install AWS SDK for S3
ARG S3_SDK_URL="https://docs.aws.amazon.com/aws-sdk-php/v3/download/aws.phar"
ARG S3_SDK_INSTALL_DIR="/usr/local/lib/php/vendor"
RUN mkdir -p "${S3_SDK_INSTALL_DIR}" && \
        curl -s "${S3_SDK_URL}" -o "${S3_SDK_INSTALL_DIR}/s3.phar"

# Enable the proxy module and related submodules
RUN a2enmod proxy proxy_http proxy_fcgi ext_filter

# Clear out the old enabled sites from sites-enabled
RUN rm /etc/apache2/sites-enabled/*

# Add new site configurations
COPY ./sites-enabled /etc/apache2/sites-enabled

# Add files for website
COPY ./public-html /var/www/html
RUN chmod -R go+rx /var/www/html && \
        mkdir -p /gallery
VOLUME /var/www/html
