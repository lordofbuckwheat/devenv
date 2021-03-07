#!/bin/bash
set -eo pipefail
_config="${1:-config.json}"
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
go build -o /root/wd/server-go main.go
cd /root/wd
./server-go --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S --config=$_config