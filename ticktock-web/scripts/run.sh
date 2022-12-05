#!/bin/sh

set -exuo pipefail

CMD="python3 -m ticktock --debug"

# Setup script for running the webserver
# Re-create the database
${CMD} destroydb
${CMD} initdb

# Create some test users, and posts for them
for i in $(seq 1 4); do
    ${CMD} genuser -i "$i"
    ${CMD} genpost -u "$i" -n 20
done

# Create a user for the user enumeration flag
${CMD} genuser -i 1097 -u "${USER_ENUMERATION_FLAG}"

# Create an admin user
${CMD} genuser -i 6114 -u admin -p "${ADMIN_PASS}"

# Create a post for the post enumeration flag
TIME="2022/01/01 00:00:00"
${CMD} genpost -u 6114 -ts "${TIME}" -te "${TIME}" -m "${POST_ENUMERATION_FLAG}" -i 1216

# Run the webserver
gunicorn -c /etc/gunicorn/gunicorn.conf.py ticktock.cmd.server:app

# ${CMD} server
