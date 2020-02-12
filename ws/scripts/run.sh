#!/bin/bash
set -eo pipefail
branch=
redirect=
norace=
while [[ -n $1 ]]; do
  case "$1" in
  -r | --redirect)
    redirect=true
    shift
    ;;
  -nr | --norace)
    norace=true
    shift
    ;;
  *)
    branch=$1
    shift
    ;;
  esac
done
checkout() {
  repo=$(basename "$(pwd)")
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
  cd /root/app/supertvbit/gopath/src/scripts
  git stash
  checkout
  cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
  git stash
  checkout
fi
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
if [[ -n $norace ]]; then
  go build -o /root/go-wd/server-go main.go
else
  go build -race -o /root/go-wd/server-go main.go
fi
cd /root/go-wd
if [[ -n $redirect ]]; then
  echo redirecting to /root/go-wd/out.log
  ./server-go --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S > /root/go-wd/out.log 2>&1
else
  ./server-go --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S
fi
