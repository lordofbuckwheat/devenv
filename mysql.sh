#!/bin/bash
set -euo pipefail
docker run -d --rm --name=mysql --mount type=bind,source=$(pwd)/dev_ws/supertvbit/master/migrations,target=/mysql/migrations --mount type=volume,source=mysql,target=/var/lib/mysql -p 13306:3306 --network=tvbitnet mysql-custom