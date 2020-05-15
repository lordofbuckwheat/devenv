#!/bin/bash
set -eo pipefail
./drop-database.sh tvbit
./drop-database.sh tvbit_test
rm -rf /root/wd/sources
rm -rf /root/wd/web
clickhouse-client -h clickhouse <<< "DROP DATABASE tvbit;"
clickhouse-client -h clickhouse <<< "CREATE DATABASE tvbit;"