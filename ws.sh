#!/bin/bash
set -euo pipefail
docker run --rm -it --name=ws --mount type=bind,source=$(pwd)/dev_config,target=/root/config --mount type=bind,source=$(pwd)/dev_src,target=/root/src --network=tvbitnet ws