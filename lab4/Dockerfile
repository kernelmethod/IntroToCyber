FROM debian:bullseye-slim

RUN apt update && \
    apt install -y john whois && \
    apt clean

ARG SPEED_USER_PREFIX="speedy"
ARG PWCRACK_USER_PREFIX="crackme"

ENV SPEED_USER_PREFIX="${SPEED_USER_PREFIX}"
ENV PWCRACK_USER_PREFIX="${PWCRACK_USER_PREFIX}"

COPY entrypoint.sh /usr/local/bin
RUN chmod a+rx,go-w /usr/local/bin/entrypoint.sh

# Run setup script
COPY --chown=root:root setup.sh /root/setup.sh
RUN chmod u+x,go-rwx /root/setup.sh && \
    /root/setup.sh


CMD [ "entrypoint.sh" ]
