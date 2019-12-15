#!/bin/bash
set -euo pipefail
cd /root/ws/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go
go build -i -race -o /root/go-wd/tvbit.ex main.go
cd /root/go-wd
./tvbit.ex --secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S