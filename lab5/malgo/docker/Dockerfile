FROM golang:1.19-alpine

# Add a user to build from source
ARG USER_UID=5000
RUN adduser builder -D -h /go -H -u $USER_UID && \
    chown -R $USER_UID:$USER_UID /go

# Install additional dependencies
RUN apk add --no-cache make musl-dev gcc git upx file

USER $USER_UID
RUN git config --global --add safe.directory '*'

# Create directories for source code and for build artifacts
ARG SRC_DIR=/go/src/mal
ENV BUILD_DIR=/go/bin
RUN mkdir -p "$SRC_DIR" && \
    mkdir -p /go/build

WORKDIR $SRC_DIR
VOLUME $SRC_DIR

CMD [ "/bin/sh", "-l" ]
