FROM debian:bullseye-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y openssh-server whois && \
    apt-get clean

ENV ENV=/etc/profile

COPY files/profile.d /etc/profile.d
RUN echo 'umask 0027' >> /etc/bash.bashrc && \
    grep -v UMASK /etc/login.defs > /tmp/login.defs && \
    mv /tmp/login.defs /etc/login.defs && \
    printf 'UMASK\t0027\n' >> /etc/login.defs

# Give SSH access to the ssh-access group
RUN groupadd -g 5000 ssh-access && \
    groupadd -g 5001 lab-users
COPY files/sshd_config /etc/ssh/sshd_config.d/

COPY scripts /usr/local/bin
RUN find /usr/local/bin -type f -exec chmod u+rx,go-w '{}' \;

# Make some changes to /etc/skel before creating users
RUN chmod -R o-rwx /etc/skel

COPY --chown=root:root passwords.txt /root/passwords.txt
RUN chmod -R go-rwx /root/passwords.txt && \
    create-users.sh /root/passwords.txt /root/passwords

# Install wordlists
RUN mkdir -p /usr/local/share/wordlists
COPY --chown=root:lab-users files/wordlist.txt /usr/local/share/wordlists/wordlist.txt

### PROBLEM 1
RUN install -o user1 -g user1 -m 400 /root/passwords/user2 /home/user1/problem.txt

### PROBLEM 2
WORKDIR /home/user2
RUN su -s /bin/bash -g user2 -c sh -c 'prob2.sh "$(cat /root/passwords/user3)"'

### PROBLEM 3
WORKDIR /home/user3

### PROBLEM 4

### PROBLEM 5

### PROBLEM 6

### PROBLEM 7

### PROBLEM 8

### PROBLEM 9

CMD [ "/usr/local/bin/docker-entrypoint.sh" ]
