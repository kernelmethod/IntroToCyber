FROM minio/mc

WORKDIR /setup

# Add user to run scripts
RUN adduser minio --shell /sbin/nologin -d /setup --password '*' --system && \
    chown -R minio /setup && \
    mkdir -p /reports && \
    chown -R minio /reports
    #chown -R root /report && \
    #chown -R root /setup

COPY entrypoint.sh ./entrypoint.sh
RUN chmod a+rx ./entrypoint.sh

COPY file_report.sh /usr/bin/file_report.sh
RUN chmod a+rx /usr/bin/file_report.sh

VOLUME /reports
USER minio
ENTRYPOINT [ "./entrypoint.sh" ]
