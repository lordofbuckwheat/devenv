#!/bin/bash
set -euo pipefail
cp config/.gitconfig ./
cp config/id_rsa ./.ssh/
if [ ! -d app/supertvbit ]; then
  cd /root/app
  git clone gitlab:g/supertvbit.git supertvbit || true
  cd /root/app/supertvbit
  git submodule init
  git submodule update
  cd /root/app/supertvbit/docs
  git checkout master --
  cd /root/app/supertvbit/gopath/src/scripts
  git checkout master --
  cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin
  git checkout master --
  cd /root/app/supertvbit/master
  git checkout master --
  cd php
  composer install
  cp /root/master-config.yml config/config.yml
  cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
  git checkout master --
  cd /root/app/supertvbit/public
  git checkout master --
  cd panel
  npm i
  npm run prod
  cd /root/waitforit
  go run main.go
  cd /root/app/supertvbit
  ./scripts/deploy.sh --hostname=https://master.tvbit.co --silent
fi
cd /root/app
zsh