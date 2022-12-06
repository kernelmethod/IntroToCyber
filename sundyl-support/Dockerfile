FROM python:3.10-slim-bullseye

ARG GECKODRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz"

# Create a directory to run the webapp
RUN mkdir -p /var/www/app && \
    adduser -G www-data -h /var/www -S -D www-data && \
    chown -R root:www-data /var/www

WORKDIR /var/www/app

# Install dependencies
RUN cd /tmp && \
    apt update && \
    apt install -y curl firefox-esr && \
    apt clean && \
    curl -s -L "${GECKODRIVER_URL}" \
        -o geckodriver.tar.gz && \
    tar xf geckodriver.tar.gz && \
    mv geckodriver /usr/local/bin && \
    apt purge -y curl

COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

# Add code
COPY --chown=root:www-data app.py .
COPY --chown=root:www-data support_handler.py .

EXPOSE 5000
CMD [ "flask", "--app", "app", "run", "--host=0.0.0.0" ]
