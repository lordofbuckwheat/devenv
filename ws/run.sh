#!/bin/bash
set -euo pipefail
cp config/.gitconfig ./
cp config/id_rsa ./.ssh/
if [ ! -d ws/supertvbit ]; then
  cd /root/ws
  git clone gitlab:g/supertvbit.git supertvbit || true
  cd /root/ws/supertvbit
  git submodule init
  git submodule update
  cd /root/ws/supertvbit/docs
  git checkout master
  cd /root/ws/supertvbit/gopath/src/scripts
  git checkout master
  cd /root/ws/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin
  git checkout master
  cd /root/ws/supertvbit/master
  git checkout master
  cd php
  composer install
  cd /root/ws/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
  git checkout master
  cd /root/ws/supertvbit/public
  git checkout master
  cd panel
  npm i
  npm run prod
fi
cd /root
zsh