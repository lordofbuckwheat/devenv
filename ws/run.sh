#!/bin/bash
set -euo pipefail
cp config/.gitconfig ./
cp config/id_rsa ./.ssh/
if [ ! -d src/supertvbit ]; then
  cd /root/src
  git clone gitlab:g/supertvbit.git supertvbit || true
  cd /root/src/supertvbit
  git submodule init
  git submodule update
  cd /root/src/supertvbit/docs
  git checkout master --
  cd /root/src/supertvbit/gopath/src/scripts
  git checkout master --
  cd /root/src/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin
  git checkout master --
  cd /root/src/supertvbit/master
  git checkout master --
  cd php
  composer install
  cp /root/master-config.yml config/
  cd /root/src/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
  git checkout master --
  cd /root/src/supertvbit/public
  git checkout master --
  cd panel
  npm i
  npm run prod
  #cd /root/src/supertvbit
  #./scripts/deploy.sh --hostname=https://master.tvbit.co
fi
cd /root
zsh