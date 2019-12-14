#!/bin/bash
set -euo pipefail
docker run --rm -d -it --name=wd --mount='type=bind,source=/home/nikita/work/devenv_config,target=/root/config' --mount='type=bind,source=/home/nikita/work/wd,target=/root/wd' wd