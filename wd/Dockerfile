FROM debian:10
RUN apt-get -y update && apt-get -y install openssh-client git zsh && apt-get clean
COPY run.sh /root
COPY sshconfig /root/.ssh/config
COPY known_hosts /root/.ssh/
WORKDIR /root
ENTRYPOINT ["./run.sh"]