#!/bin/bash

set -euo pipefail

create_user() {
    PASSWORD="$1"
    USER_ID="$2"

    # Create a new user with the provided password
    set -x

    useradd "${USERNAME_PREFIX}${USER_ID}" \
        --uid $((${BASE_UID} + ${USER_ID})) \
        --password "${PASSWORD}" \
        --shell $(which nologin) \
        --home-dir / \
        --no-create-home \
        --no-user-group

    set +x
}


####################################################################
#
# Speed problems
#

# Create four users with the same password, but with different hashing algorithms:
# - MD5
# - SHA-256, 1000 rounds
# - SHA-256, 5000 rounds
# - yescrypt

USERNAME_PREFIX="${SPEED_USER_PREFIX:-speedy}"
BASE_UID=2000
SPEED_PASSWORD="idunno"

i=1

create_user $(echo -n "${SPEED_PASSWORD}" | mkpasswd -m md5crypt -s) $i
i=$(($i + 1))

create_user $(echo -n "${SPEED_PASSWORD}" | mkpasswd -m sha512crypt -R 1000 -s) $i
i=$(($i + 1))

create_user $(echo -n "${SPEED_PASSWORD}" | mkpasswd -m sha512crypt -R 10000 -s) $i
i=$(($i + 1))

create_user $(echo -n "${SPEED_PASSWORD}" | mkpasswd -m yescrypt -s) $i
i=$(($i + 1))

####################################################################
#
# Password cracking problems
#

USERNAME_PREFIX="${PWCRACK_USER_PREFIX:-crackme}"
FORMAT=sha256crypt
BASE_UID=3000
i=1

# Create a user whose password is $password!?
# $password = pinky14
create_user $(echo -n "pinky14!?" | mkpasswd -m "${FORMAT}" -s) $i
i=$(($i + 1))

# Create a user whose password is flag{$password}
# $password = hearts!
create_user $(echo -n "flag{hearts!}" | mkpasswd -m "${FORMAT}" -s) $i
i=$(($i + 1))

# Create a user whose password is $password$bits
# $password = 160891
# $bits = 0011
create_user $(echo -n "1608910011" | mkpasswd -m "${FORMAT}" -s) $i
i=$(($i + 1))

# Create a user whose password is $Season$Year$password!
# $Season = Summer
# $Year = 2022
# $password = sherin
create_user $(echo -n "Summer2022sherin!" | mkpasswd -m "${FORMAT}" -s) $i
i=$(($i + 1))

# Create a user whose password is $month$capitalize(password)
# $month = March
# $password = karla123
create_user $(echo -n "MarchKarla123" | mkpasswd -m "${FORMAT}" -s) $i
i=$(($i + 1))
