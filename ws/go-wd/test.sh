#!/bin/bash
set -eo pipefail
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
pattern=${1}
if [[ -z "${pattern}" ]]; then
  go test --race -v -c -o /root/go-wd/server-go.test --run "${pattern}"
else
  go test --race -v -c -o /root/go-wd/server-go.test
fi
cd /root/go-wd
./server-go.test --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S