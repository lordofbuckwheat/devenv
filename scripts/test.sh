#!/bin/bash
set -eo pipefail
pattern=
norace=
while [[ -n $1 ]]; do
  case "$1" in
  -nr | --norace)
    norace=true
    shift
    ;;
  *)
    pattern=$1
    shift
    ;;
  esac
done
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
if [[ -n $norace ]]; then
  go test -v -c -o /root/wd/server-go.test gitlab.tvbit.co/g/server-go
else
  go test --race -v -c -o /root/wd/server-go.test gitlab.tvbit.co/g/server-go
fi
cd /root/wd
echo redirecting to /root/wd/test.log
if [[ -z "${pattern}" ]]; then
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S > /root/wd/test.log 2>&1
else
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S -test.run "${pattern}" > /root/wd/test.log 2>&1
fi