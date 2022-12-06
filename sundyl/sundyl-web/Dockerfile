FROM python:3.10-alpine

# Create a directory to run the webapp
RUN mkdir -p /var/www/app && \
    mkdir -p /var/www/static && \
    mkdir -p /var/www/media && \
    adduser -G www-data -h /var/www -S -D www-data && \
    chown -R root:www-data /var/www && \
    chown -R www-data:www-data /var/www/static /var/www/media && \
    chmod -R g+rx /var/www

WORKDIR /var/www/app

# Create directory for gunicorn configuration
RUN mkdir -p /usr/share/gunicorn && chown -R root:www-data /usr/share/gunicorn

COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

# Add management script
COPY --chown=root:www-data manage.py .

# Add entrypoint script
COPY --chown=root:www-data entrypoint.sh /entrypoint.sh
RUN chmod ug+rx /entrypoint.sh

# Add Gunicorn config
COPY --chown=root:www-data conf/gunicorn.conf.py /usr/share/gunicorn/gunicorn.conf.py

# Add code and static files
COPY --chown=root:www-data sundyl/ ./sundyl
COPY --chown=root:www-data static/ ./static

CMD [ "/entrypoint.sh" ]
