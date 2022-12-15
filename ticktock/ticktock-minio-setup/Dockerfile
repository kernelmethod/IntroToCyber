FROM minio/mc:latest

WORKDIR /setup
COPY . .
RUN chmod a+rx,go-w ./setup.sh

ENTRYPOINT [ "/setup/setup.sh" ]
