#!/bin/bash

source versions.sh

set -eu
set -o pipefail

docker ps -q --filter "name=bifrost_underground" | grep -q . && sleep 1 && docker stop bifrost_underground && sleep 5 && docker rm -fv bifrost_underground && sleep 5



docker build --rm \
        --build-arg ftp_proxy \
        --build-arg http_proxy \
        --build-arg https_proxy \
	--build-arg bifrost_version=${BIFROST_VERSION} \
	--build-arg ansible_version=${ANSIBLE_VERSION} \
	--build-arg testing=${TESTING} \
	--build-arg cli=${CLI} \
	--build-arg usedib=${USEDIB} \
        -t underground-bifrost:$BIFROST_TAG \
	../
