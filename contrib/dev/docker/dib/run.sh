#!/bin/bash

WORKDIR="$HOME/workspace/PROD/underground"

ELEMENTS_DIR="$WORKDIR/elements"
SHARED_DIR="$WORKDIR/shared"

docker run --rm -it --name underground_dib \
	--privileged \
	-v $ELEMENTS_DIR:/underground/elements:ro \
	-v $SHARED_DIR:/shared:rw \
	-e container=docker \
        underground_dib:latest bash #disk-image-create virtual ubuntu docker-engine cloud-user -o $SHARED_DIR/ubuntu-focal-builder
