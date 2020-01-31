#!/bin/bash
set -eo pipefail
./drop-client.sh
rsync -var --delete `find dump/apidata/ -maxdepth 1 -type d | grep -P 'apidata\/\d+$'` /root/app/supertvbit/public/public/api/apidata
./drop-database.sh tvbit dump/sql/tvbit.sql
./drop-database.sh tvbit_test dump/sql/tvbit_test.sql