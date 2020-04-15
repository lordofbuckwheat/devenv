#!/bin/bash
set -eo pipefail
subcommand=$1
shift
redirect=
race=
allParams=()
while [[ -n $1 ]]; do
  case "$1" in
  -r | --redirect)
    redirect=true
    shift
    ;;
  --race)
    race=true
    shift
    ;;
  *)
    allParams+=("$1")
    shift
    ;;
  esac
done
cd /root/app/supertvbit/gopath/src/scripts/clientemulator
if [[ -n $race ]]; then
  go build --race -o /root/wd/client .
else
  go build -o /root/wd/client .
fi
cd /root/wd
if [[ -n $redirect ]]; then
  echo redirecting to /root/wd/out-client.log
  ./client "$subcommand" "${allParams[@]}" >/root/wd/out-client.log 2>&1
else
  ./client "$subcommand" "${allParams[@]}"
fi
