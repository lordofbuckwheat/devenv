#!/bin/bash
until [[ -d /mysql/app/supertvbit/master/migrations ]]; do
  echo master migration is unavailable - sleeping
  sleep 1
done
docker-entrypoint.sh mysqld