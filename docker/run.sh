#!/bin/bash
set -e
set -u

SCRIPTROOT="$( cd "$(dirname "$0")" ; pwd -P )"

echo "running docker without display"
docker run -it  -v ${SCRIPTROOT}/..:/workspace/biliAgent -v /home:/home \
--shm-size 64G \
--network=host \
--gpus=all \
--name=bilagent biliagent /bin/bash
# --network=bridge \
# -p 8000:8000 \
# -p 8501:8501 \
# --env http_proxy=172.17.0.1:7897 \
# --env https_proxy=172.17.0.1:7897 \