#!/bin/bash
set -eo pipefail
clickhouse-client -h clickhouse <<< "DROP DATABASE tvbit;"
clickhouse-client -h clickhouse <<< "CREATE DATABASE tvbit;"
rsync -var --delete `find dump/apidata/ -maxdepth 1 -type d | grep -P 'apidata\/(\d+|converted_videos|thumbs)$'` /root/app/supertvbit/public/public/api/apidata
./drop-database.sh tvbit dump/sql/tvbit.sql
./drop-database.sh tvbit_test dump/sql/tvbit_test.sql