FROM alpine:3.16

RUN apk add --no-cache rclone fuse

COPY entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh

CMD [ "/entrypoint.sh" ]
