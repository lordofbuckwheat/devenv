FROM nginx:1.17.6
WORKDIR /root
COPY sites-enabled /etc/nginx/sites-enabled
COPY nginx.conf /etc/nginx/
RUN mkdir logs && mkdir logs/master && mkdir logs/public