#!/bin/bash
set -euo pipefail
docker run --rm -d -it --name=wd --mount type=bind,source=$(pwd)/dev_config,target=/root/config --mount type=bind,source=$(pwd)/dev_wd,target=/root/wd wd