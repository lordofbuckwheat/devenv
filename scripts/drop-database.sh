#!/bin/bash
set -eo pipefail
db_name=${1}
sql="DROP DATABASE IF EXISTS ${db_name}; CREATE DATABASE ${db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
mysql -u root -p'root' -h mysql <<< "${sql}"
dump=${2}
if [[ -f "${dump}" ]]; then
    mysql -u root -p'root' -h mysql ${db_name} < "${dump}"
fi