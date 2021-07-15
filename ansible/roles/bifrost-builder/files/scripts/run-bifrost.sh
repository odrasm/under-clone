#!/bin/bash

source versions.sh


docker run --rm -d --name bifrost_underground \
	$CAPABILITIES \
	--cap-add=SYS_ADMIN \
	--cap-add=NET_ADMIN \
	--cap-add=SYSLOG \
	--cap-add=NET_BROADCAST \
	--cap-add=SYS_MODULE \
	--tmpfs /tmp \
	--tmpfs /run \
	--tmpfs /run/lock \
	-v /sys/fs/cgroup:/sys/fs/cgroup:ro \
	--stop-signal SIGRTMIN+3 \
	-e container=docker \
        --mount source=bifrost_httpboot,destination=/httpboot \
        --mount source=bifrost_mysql,destination=/var/lib/mysql \
        --mount source=bifrost_tftpboot,destination=/tftpboot \
        --mount source=bifrost_ironic,destination=/etc/ironic \
        --mount source=bifrost_ironiclib,destination=/var/lib/ironic \
	-v $SHARED_DIR:/bifrost/host_configs:rw \
       underground-bifrost:${BIFROST_RELEASE:-latest}

