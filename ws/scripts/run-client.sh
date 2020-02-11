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
cd /root/app/supertvbit/gopath/src/scripts/device-emulator
go build -o /root/go-wd/device-emulator .
cd /root/go-wd
if [[ -n $redirect ]]; then
  echo redirecting to /root/go-wd/out-client.log
  ./device-emulator "${allParams[@]}" >/root/go-wd/out-client.log 2>&1
else
  ./device-emulator "${allParams[@]}"
fi
