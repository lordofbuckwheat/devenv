#!/bin/bash
until [[ -d /mysql/app/supertvbit/master/migrations ]]; do
  echo master migrations is unavailable - sleeping
  sleep 1
done
docker-entrypoint.sh mysqld