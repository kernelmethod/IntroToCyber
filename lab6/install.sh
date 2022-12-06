#!/bin/bash

###
### Installation script for Lab 6
###

INSTALL_DIR=/usr/local/share/cs3710
LAB_USER="${LAB_USER}"

set -euo pipefail

if [ ! $(id -u) -eq 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

addline() {
    grep -qxF "$1" "$2" || echo "$1" >> "$2"
}

set -x

mkdir -p "${INSTALL_DIR}"
chown -R "${LAB_USER}:${LAB_USER}" "${INSTALL_DIR}"
sudo -u "${LAB_USER}" rsync -Pavz \
    --delete \
    --exclude="solution" \
    --exclude="vcr*.sh" \
    --chmod="a+r,go-w" \
    . "${INSTALL_DIR}"

# Install the AppArmor profiles
install -o root -g root -m 644 profiles/sandbox.profile /etc/apparmor.d/sandbox.profile
install -o root -g root -m 644 profiles/vuln.profile    /etc/apparmor.d/vuln.profile

apparmor_parser -Kr /etc/apparmor.d/sandbox.profile
apparmor_parser -Kr /etc/apparmor.d/vuln.profile

aa-complain /etc/apparmor.d/sandbox.profile
aa-complain /etc/apparmor.d/vuln.profile

# Get rid of some of the abstractions files that are more likely to be confusing
# than not
rm -f /etc/apparmor.d/abstractions/lightdm
rm -f /etc/apparmor.d/abstractions/dovecot-common
rm -f /etc/apparmor.d/abstractions/postfix-common

addline '127.0.0.1              www.tws.lab' /etc/hosts
addline '127.0.0.1      sundyl4ever.tws.lab' /etc/hosts
addline '127.0.0.1          malware.tws.lab' /etc/hosts
addline '127.0.0.1              www.tws.lab' /etc/cloud/templates/hosts.debian.templ
addline '127.0.0.1      sundyl4ever.tws.lab' /etc/cloud/templates/hosts.debian.templ
addline '127.0.0.1          malware.tws.lab' /etc/cloud/templates/hosts.debian.templ

cat << EOF | tee /etc/profile.d/50-lab.sh
export no_proxy=.lab,\${no_proxy}
export NO_PROXY=\${no_proxy}
EOF
