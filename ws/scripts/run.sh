#!/bin/bash
set -eo pipefail
branch=$1
checkout() {
  repo=$(basename $(pwd))
  if git checkout ${branch} --; then
    echo $repo checked out to $branch
  else
    if [[ ${branch} == hotfix/* ]]; then
      git checkout master --
      echo $repo checked out to master
    else
      git checkout develop --
      echo $repo checked out to develop
    fi
  fi
  git pull
}
if [[ ! -z ${branch} ]]; then
  ./drop-client.sh
  cd /root/app/supertvbit/public
  git stash
  checkout
  cd panel
  npm i
  npm run prod
  cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
  git stash
  checkout
fi
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
go build -i -race -o /root/go-wd/server-go main.go
cd /root/go-wd
./server-go --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S