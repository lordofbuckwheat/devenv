#!/bin/bash
set -eo pipefail
docker-compose down
sudo rm -rf app
docker volume rm devenv_mysql || true
docker volume rm devenv_clickhouse || true
docker volume rm devenv_go_modules || true
docker volume rm devenv_pip_packages || true
docker volume rm devenv_pipenv_packages || true