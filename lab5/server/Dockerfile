FROM python:3-alpine

ARG APP_DIR=/var/opt/lab5
ARG APP_USER=lab
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

# Create a directory for .pyc files
RUN mkdir -p /var/cache/pycache && \
    chown -R "${APP_USER}:${APP_USER}" /var/cache/pycache
ENV PYTHONPYCACHEPREFIX=/var/cache/pycache

# Install dependencies
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

# Copy application code and install dependencies
COPY --chown="${APP_USER}:${APP_USER}" . "${APP_DIR}/"

# Run the web server on application start
VOLUME /etc/gunicorn
VOLUME ./lab5

CMD [ "gunicorn", "-c", "/etc/gunicorn/gunicorn.conf.py", "lab5:app" ]
