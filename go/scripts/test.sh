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
cd /app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
if [[ -n $norace ]]; then
  go test -v -c -o /go-wd/server-go.test gitlab.tvbit.co/g/server-go
else
  go test --race -v -c -o /go-wd/server-go.test gitlab.tvbit.co/g/server-go
fi
cd /go-wd
echo redirecting to /go-wd/test.log
if [[ -z "${pattern}" ]]; then
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S > /go-wd/test.log 2>&1
else
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S -test.run "${pattern}" > /go-wd/test.log 2>&1
fi