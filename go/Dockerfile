FROM golang:1.13-stretch
SHELL ["/bin/bash", "-c"]
COPY scripts /scripts
COPY ssl /ssl
RUN mv /ssl/rootCA.crt /usr/local/share/ca-certificates/ && update-ca-certificates
WORKDIR /scripts