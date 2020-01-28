FROM debian:10
SHELL ["/bin/bash", "-c"]
WORKDIR /root
RUN apt-get -y update && apt-get -y install openssh-client git zsh gcc wget xz-utils locales nano curl unzip php7.3 php7.3-curl php7.3-dom php7.3-dev libmcrypt-dev php-pear zip unzip aptitude default-mysql-client clickhouse-client screen rsync && apt-get clean
RUN wget -O node.tar.xz https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz && tar -xf node.tar.xz && rm node.tar.xz
RUN wget -O ffmpeg.zip https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.2.1/ffmpeg-4.2.1-linux-64.zip && unzip ffmpeg.zip && rm ffmpeg.zip && rm -r __MACOSX
RUN wget -O go.tar.gz -- https://dl.google.com/go/go1.13.5.linux-amd64.tar.gz && tar -xf go.tar.gz && rm go.tar.gz && mkdir gopath
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN pecl channel-update pecl.php.net && pecl install channel://pecl.php.net/mcrypt-1.0.2
COPY php.ini /etc/php/7.3/cli/
COPY composer.phar /usr/local/bin/composer
ENV GOROOT /root/go
ENV GOPATH /root/gopath
ENV PATH $PATH:/root/go/bin:/root/node-v10.16.0-linux-x64/bin
RUN npm config set unsafe-perm true && npm install -g gulp
COPY go-wd /root/_go-wd
RUN mv ffmpeg _go-wd/
COPY ssl /root/ssl
RUN mv /root/ssl/rootCA.crt /usr/local/share/ca-certificates/ && update-ca-certificates
COPY .ssh /root/.ssh
COPY waitforit /root/waitforit
COPY scripts /root/scripts
COPY uploaddummies /root/uploaddummies
COPY master-config.yml panel_config.json run.sh .zshrc .screenrc tvbit.licenses.key /root/
ENTRYPOINT ["./run.sh"]