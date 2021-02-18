#!/bin/bash

SRCDIR="$HOME/workspace/PROD/underground"
SSHKEYPATH="$HOME/.ssh"

docker run --rm --name underground_toolbox -v "$SSHKEYPATH:/root/.ssh:ro" -v "$SRCDIR:/root/underground:rw" -it underground-toolbox:1.0 bash
