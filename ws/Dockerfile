FROM debian:10
SHELL ["/bin/bash", "-c"]
WORKDIR /root
RUN apt-get -y update && apt-get -y install openssh-client git zsh gcc wget xz-utils locales nano curl unzip php7.3 php7.3-curl php7.3-dom php7.3-dev libmcrypt-dev php-pear zip unzip && apt-get clean
RUN wget -O node.tar.xz https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz && tar -xf node.tar.xz && rm node.tar.xz
RUN wget -O ffmpeg.zip https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.2.1/ffmpeg-4.2.1-linux-64.zip && unzip ffmpeg.zip && rm ffmpeg.zip && rm -r __MACOSX
RUN wget -O go.tar.gz -- https://dl.google.com/go/go1.13.5.linux-amd64.tar.gz && tar -xf go.tar.gz && rm go.tar.gz && mkdir gopath
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY go-wd /root/go-wd
RUN pecl channel-update pecl.php.net && pecl install channel://pecl.php.net/mcrypt-1.0.2
COPY php.ini /etc/php/7.3/cli/
COPY composer.phar /usr/local/bin/composer
RUN mv ffmpeg go-wd/
ENV GOROOT /root/go
ENV GOPATH /root/gopath
ENV PATH $PATH:/root/go/bin:/root/node-v10.16.0-linux-x64/bin
RUN npm config set unsafe-perm true && npm install -g gulp
COPY .ssh /root/.ssh
COPY master-config.yml run.sh .zshrc /root/
ENTRYPOINT ["./run.sh"]