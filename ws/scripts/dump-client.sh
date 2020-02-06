#!/bin/bash
set -eo pipefail
mkdir -p dump/apidata
rsync -var --delete `find /root/app/supertvbit/public/public/api/apidata/ -maxdepth 1 -type d | grep -P 'apidata\/(\d+|converted_videos|thumbs)$'` dump/apidata
mkdir -p dump/sql
mysqldump -u root -proot -h mysql tvbit > dump/sql/tvbit.sql
mysqldump -u root -proot -h mysql tvbit_test > dump/sql/tvbit_test.sql