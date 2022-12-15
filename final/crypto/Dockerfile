FROM python:3.10-alpine

ARG UID=29598
RUN adduser -D -h /var/www -u $UID crypto

WORKDIR /var/www
COPY --chown=$UID:$UID requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chown root:root /usr/local/bin/docker-entrypoint.sh && \
    chmod a+rx,go-w /usr/local/bin/docker-entrypoint.sh

COPY --chown=$UID:$UID cryptoapi ./cryptoapi
COPY --chown=$UID:$UID tests.py .

CMD [ "/usr/local/bin/docker-entrypoint.sh" ]
