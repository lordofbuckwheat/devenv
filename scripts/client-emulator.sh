#!/bin/bash
set -eo pipefail
cd /home/nikita/devenv/app/supertvbit/gopath/src/scripts/clientemulator
go build -o /home/nikita/devenv/wd/clientemulator main.go
cd /home/nikita/devenv/wd
/home/nikita/devenv/wd/clientemulator $@
