#!/bin/bash
set -eo pipefail
subcommand=$1
shift
redirect=
allParams=()
while [[ -n $1 ]]; do
  case "$1" in
  -r | --redirect)
    redirect=true
    shift
    ;;
  *)
    allParams+=("$1")
    shift
    ;;
  esac
done
cd /root/app/supertvbit/gopath/src/scripts/clientemulator
go build -o /root/wd/client .
cd /root/wd
if [[ -n $redirect ]]; then
  echo redirecting to /root/wd/clientemulator.log
  ./client "$subcommand" "${allParams[@]}" >/root/wd/clientemulator.log 2>&1
else
  ./client "$subcommand" "${allParams[@]}"
fi
