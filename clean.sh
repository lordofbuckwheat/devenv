#!/bin/bash
set -euo pipefail
docker-compose down
sudo rm -rf app go-wd
docker volume rm devenv_mysql || true
docker volume rm devenv_clickhouse || true
docker volume rm devenv_go_modules || true