#!/bin/bash
set -eo pipefail
pattern=${1}
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
go test --race -v -c -o /root/go-wd/server-go.test gitlab.tvbit.co/g/server-go
cd /root/go-wd
if [[ -z "${pattern}" ]]; then
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S
else
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S -test.run "${pattern}"
fi