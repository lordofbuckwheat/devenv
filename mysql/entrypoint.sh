#!/bin/bash
until [[ -e /mysql/app/supertvbit/master/migrations/ready ]]; do
  echo master migration is unavailable - sleeping
  sleep 1
done
docker-entrypoint.sh mysqld