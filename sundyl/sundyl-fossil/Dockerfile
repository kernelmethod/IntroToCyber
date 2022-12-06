FROM alpine:3.16

RUN apk add --no-cache fossil lighttpd

# Create a user to run fossil + lighttpd
RUN addgroup fossil && \
    adduser -G fossil -h /opt/fossil -S -D fossil && \
    mkdir -p /var/opt/lighttpd && \
    mkdir -p /var/opt/fossil && \
    chown -R fossil:fossil /var/opt/fossil /var/opt/lighttpd && \
    chown -R fossil:fossil /var/log/lighttpd

# Add CGI scripts
RUN mkdir -p /var/www/html && chown -R fossil:fossil /var/www
COPY --chown=fossil:fossil cgi-bin /var/www/cgi-bin

# Add a script to export the repository configuration
COPY export_config.sh /usr/local/bin
RUN chmod a+rx,go-w /usr/local/bin/export_config.sh

# Configure the lighttpd server
COPY lighttpd /etc/lighttpd
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+rx /entrypoint.sh

USER fossil
ENV USER="fossil"
WORKDIR /opt/fossil

# Initialize and open the repository
RUN mkdir repos && \
    cd repos && \
    fossil init -A fossil scm.fossil | tee /var/opt/fossil/output.log && \
    fossil open scm.fossil && \
    fossil user default fossil

# Extract password into a separate file
RUN cd /var/opt/fossil && \
    sed -n 's/.*initial password is "\(.*\)")$/\1/p' output.log > password.txt

WORKDIR /opt/fossil/repos

# Import the project configuration
COPY project_config.txt /var/opt/fossil/project_config.txt
RUN fossil config import /var/opt/fossil/project_config.txt

# Copy in wiki pages and commit them to the repo
COPY --chown=fossil:fossil ./www ./www
RUN fossil user default fossil && \
    fossil add ./www && \
    fossil commit -m "Initial commit."

# Run a script to set up tickets, etc.
COPY --chown=fossil:fossil setup.sh /var/opt/fossil
RUN chmod u+x,go-rwx /var/opt/fossil/setup.sh && \
    /var/opt/fossil/setup.sh

RUN chmod ug+rx /var/www/cgi-bin/*
CMD [ "/entrypoint.sh" ]
