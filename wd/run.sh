#!/bin/bash
set -euo pipefail
cp config/.gitconfig ./
cp config/id_rsa ./.ssh/
cd wd
if [ ! -d supertvbit ]; then
  git clone gitlab:g/supertvbit.git supertvbit || true
  cd supertvbit
  git submodule init
  git submodule update
  cd /root/wd/supertvbit/docs
  git checkout master
  cd /root/wd/supertvbit/gopath/src/scripts
  git checkout master
  cd /root/wd/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin
  git checkout master
  cd /root/wd/supertvbit/master
  git checkout master
  cd /root/wd/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
  git checkout master
  cd /root/wd/supertvbit/public
  git checkout master
  cd /root/wd
fi
zsh