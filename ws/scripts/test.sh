#!/bin/bash
set -eo pipefail
pattern=${1}
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
go test --race -v -c -o /root/go-wd/server-go.test gitlab.tvbit.co/g/server-go
cd /root/go-wd
echo redirecting to /root/go-wd/test.log
if [[ -z "${pattern}" ]]; then
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S > /root/go-wd/test.log 2>&1
else
  ./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S -test.run "${pattern}" > /root/go-wd/test.log 2>&1
fi