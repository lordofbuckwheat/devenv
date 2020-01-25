#!/bin/bash
set -euo pipefail
cd /root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
go build -i -race -o /root/go-wd/server-go main.go
cd /root/go-wd
./server-go --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S