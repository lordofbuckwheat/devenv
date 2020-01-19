#!/bin/bash
set -euo pipefail
docker run -d --rm --name=php --mount type=bind,source=$(pwd)/dev_src/supertvbit/master/php,target=/root/web/master --network=tvbitnet php-custom