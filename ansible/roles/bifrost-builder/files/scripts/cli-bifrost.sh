#!/bin/bash

source versions.sh
WORKDIR="bifrost"

docker exec -it bifrost /bifrost/bifrost-cli $DEBUG "$@"
