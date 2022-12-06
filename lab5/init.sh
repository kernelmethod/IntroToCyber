#!/bin/bash

set -euo pipefail

N_USERS=200
UID_BASE=10000

MNAMES=/usr/share/seclists/Usernames/Names/malenames-usa-top1000.txt
FNAMES=/usr/share/seclists/Usernames/Names/femalenames-usa-top1000.txt
NAMES=$(cat $MNAMES $FNAMES | tr '[:upper:]' '[:lower:]' | sort | uniq | shuf -n${N_USERS})

USER_HOME_ROOT=/u

# Update sysctl config
cp -v sysctl.d/* /etc/sysctl.d/

# Install student driver
if [ -f driver ]; then
    install -o root -g root -m 755 driver /usr/local/bin/driver

    # Override DAC on the driver so that it can read privilieged files
    setcap cap_dac_override=+eip /usr/local/bin/driver
else
    echo "driver binary not found; did you build it?" >&2
fi

# Install base firewall configuration
mkdir -p /usr/local/share/cs3710
cp -v base.nft /usr/local/share/cs3710

# Store home directories in /u
mkdir -p /u

i=1
for name in $NAMES; do
    uid=$(($UID_BASE+$i))
    i=$(($i+1))

    if ! id -u "$uid" >/dev/null 2>&1; then
        echo "Creating user $name (uid = $uid)"
        useradd "$name" \
            --password '!' \
            --uid "$uid" \
            --create-home \
            --home-dir "/u/$name"
    fi
done

# Clean out mailboxes
find /var/mail -type f -exec rm '{}' +

UIDS=$(seq $(($UID_BASE+1)) $(($UID_BASE+$N_USERS)))
CRONTAB=$(printf 'MAILTO=""\n')
CRONTAB=$(printf "${CRONTAB}\n*/2 * * * * /usr/local/bin/driver\n")

echo "Crontab:"
echo "$CRONTAB"

for uid in $UIDS; do
    echo "Adding crontab for user $uid"
    sudo -u "#$uid" sh -c "echo '${CRONTAB}' | crontab -"
done
