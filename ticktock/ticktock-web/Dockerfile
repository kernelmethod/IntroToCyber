FROM python:3.10-alpine

ARG APP_DIR=/var/opt/ticktock
ARG APP_USER=ticktock
ARG APP_USER_UID=1000

# Create a user to run the web server
RUN mkdir -p "${APP_DIR}" && \
        addgroup "${APP_USER}" && \
        adduser "${APP_USER}" \
            -H -S -D \
            -G "${APP_USER}" \
            -s /bin/false \
            -h "${APP_DIR}" \
            -u "${APP_USER_UID}" && \
        chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}"

# Create important paths
RUN mkdir -p "/var/log/ticktock" && \
        chown -R "${APP_USER}:${APP_USER}" "/var/log/ticktock" && \
        mkdir "/scripts" && \
        chown -R "${APP_USER}:${APP_USER}" "/scripts"

# Install dependencies
RUN apk add --no-cache libmagic postgresql14-client
COPY requirements.txt /tmp
RUN apk add --no-cache --virtual build-deps build-base musl-dev && \
        pip install --no-cache-dir -r /tmp/requirements.txt && \
        apk del build-deps

# Install configuration for gunicorn
RUN mkdir -p /etc/gunicorn
COPY conf/gunicorn.conf.py /etc/gunicorn/gunicorn.conf.py
RUN chown -R "root:${APP_USER}" /etc/gunicorn && \
        chmod -R g+r,g-w /etc/gunicorn

USER "${APP_USER}"
WORKDIR "${APP_DIR}"

# Add setup script
COPY --chown="${APP_USER}:${APP_USER}" scripts/run.sh /scripts/run.sh

# Copy application code and install dependencies
COPY --chown="${APP_USER}:${APP_USER}" . "${APP_DIR}/"

# Run the web server on application start
VOLUME /etc/gunicorn
VOLUME ./ticktock
VOLUME /scripts

CMD [ "python", "-m", "ticktock", "--debug", "server" ]
