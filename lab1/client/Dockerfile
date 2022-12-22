FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y openssh-client && \
    apt-get clean

RUN useradd client --uid 5000 \
        --create-home \
        --shell /bin/bash  \
        --password '!'

USER client
WORKDIR /home/client
CMD [ "tail", "-f", "/dev/null" ]
