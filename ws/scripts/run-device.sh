#!/bin/bash
set -eo pipefail
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
cd /root/app/supertvbit/gopath/src/scripts/clientemulator/device
go build -o /root/go-wd/device .
cd /root/go-wd
if [[ -n $redirect ]]; then
  echo redirecting to /root/go-wd/out-device.log
  ./device "${allParams[@]}" >/root/go-wd/out-device.log 2>&1
else
  ./device "${allParams[@]}"
fi
