FROM nginx:1.25-alpine

# Remove the default enabled site configurations
RUN rm /etc/nginx/conf.d/*.conf

COPY snippets /etc/nginx/snippets

COPY run.sh /run.sh
RUN chmod u+x,go-rwx /run.sh

COPY nginx.conf /etc/nginx/nginx.conf
COPY conf/ /etc/nginx/conf.d
COPY 404.html /var/www/html

RUN chmod -R a+r /etc/nginx

CMD [ "/run.sh" ]
