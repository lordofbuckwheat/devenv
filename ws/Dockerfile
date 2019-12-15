FROM debian:10
SHELL ["/bin/bash", "-c"]
WORKDIR /root
RUN apt-get -y update && apt-get -y install openssh-client git zsh gcc wget xz-utils locales nano curl && apt-get clean
RUN wget -O go.tar.gz -- https://dl.google.com/go/go1.13.5.linux-amd64.tar.gz && tar -xf go.tar.gz && rm go.tar.gz && wget -O node.tar.xz https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz && tar -xf node.tar.xz && rm node.tar.xz
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY run.sh .zshrc /root/
COPY .ssh /root/.ssh
COPY .oh-my-zsh /root/.oh-my-zsh
COPY go-wd /root/go-wd
ENV PATH $PATH:/root/go/bin:/root/node-v10.16.0-linux-x64/bin
RUN npm config set unsafe-perm true
ENTRYPOINT ["./run.sh"]