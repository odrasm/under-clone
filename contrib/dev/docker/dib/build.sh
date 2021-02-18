#!/bin/bash

set -eu
set -o pipefail

docker ps -q --filter "name=underground_dib" | grep -q . && sleep 1 && docker stop underground_dib && sleep 5 && docker rm -fv underground_dib && sleep 5



docker build --rm \
        --build-arg ftp_proxy \
        --build-arg http_proxy \
        --build-arg https_proxy \
        -t underground_dib \
	../dib

