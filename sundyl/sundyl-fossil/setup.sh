#!/bin/sh

set -ex

REPO="-R /opt/fossil/repos/scm.fossil"

# Ticket info: https://fossil-scm.org/home/doc/trunk/www/tickets.wiki

# Create a ticket for adding the Docker provider for Apache Airflow
# fossil ticket ${REPO} add \
#     username "${USER}" \
#     status "Fixed" \
#     severity "Minor" \
#     subsystem "Airflow" \
#     type "Feature_Request" \
#     title "Add Docker provider to Airflow" \
#     comment "\
# It looks like you can add support for Docker operators to Apache Airflow with the
# Airflow Docker provider:
# 
#     https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/index.html
# 
# Let's get that set up sometime in the near future. While you're at it, maybe you
# can set up some of apache-airflow-providers-docker's example DAGs so that we can
# play around with Docker operators before we integrate them into the product.
# "

# Set icomment to add a comment to the ticket
fossil ticket ${REPO} add \
    username "${USER}" \
    status "Closed" \
    severity "Minor" \
    subsystem "Website" \
    type "Feature_Request" \
    title "File reports" \
    comment "\
Now that we've got the file uploads working correctly for the main site, we should
make sure that nobody is uploading malicious stuff in there. I'd like to set up
a script that goes through and lists the files, and maybe runs some additional
administrative scripts to get collect information against them.

Could we get that set up sometime in the near future? I was thinking perhaps we
could get it hosted on reports.sundyl.lab
"


# Create a new ticket for the Airflow password
fossil ticket ${REPO} add \
    username "${USER}" \
    status "Open" \
    severity "Severe" \
    subsystem "MinIO" \
    type "Incident" \
    title "Changing MinIO usernames" \
    comment "\
Right now we're just doing everything with the same \"minio\" user on MinIO.
Having everyone use the same privileged account puts us at risk if one of us
is compromised. MinIO comes with AWS-compatible IAM that we should look into.

- Jodi
"

# Create a ticket for CVE-2022-38362
fossil ticket ${REPO} add \
    username "${USER}" \
    status "Open" \
    severity "Critical" \
    subsystem "Website" \
    type "Incident" \
    title "Stop using the same passwords for everything!!!!" \
    comment "\
Freddy -- I'm not sure how many times I need to tell you, but putting the current
season and year at the front of your password is not a good way to secure your
password. In particular,

Fall2022password123!

is not a safe password. Please change it ASAP, both on th website and elsewhere.

- Jodi
"


# Create new users
# Jodi Crockwell
fossil user ${REPO} new jcrockwell '' ''

# Freddy Obrzut
fossil user ${REPO} new fobrzut '' ''

# Kirby Elledge
fossil user ${REPO} new kelledge '' ''

