FROM postgres:14

# Add entrypoint scripts
COPY init_users.sh /docker-entrypoint-initdb.d/init_users.sh
RUN chmod a+rx /docker-entrypoint-initdb.d/init_users.sh
