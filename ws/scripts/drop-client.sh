#!/bin/bash
set -eo pipefail
./drop-database.sh tvbit
./drop-database.sh tvbit_test
rm -rf /root/app/supertvbit/public/public/api/apidata/1
rm -rf /root/app/supertvbit/public/public/api/apidata/2
rm -rf /root/app/supertvbit/public/public/api/apidata/3
rm -rf /root/app/supertvbit/public/public/api/apidata/converted_videos
rm -rf /root/app/supertvbit/public/public/api/apidata/thumbs
rm -rf /root/go-wd/sources
rm -rf /root/go-wd/web
clickhouse-client -h clickhouse <<< "DROP DATABASE tvbit;"
clickhouse-client -h clickhouse <<< "CREATE DATABASE tvbit;"