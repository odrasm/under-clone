#!/bin/bash

source versions.sh

BIFROST_VOLUMES="bifrost_httpboot, bifrost_mysql, bifrost_tftpboot, bifrost_ironic"

docker ps -q --filter "name=bifrost" | grep -q . && sleep 1 && docker stop bifrost && sleep 5 && docker rm -fv bifrost && sleep 5

sleep 1

docker volume create bifrost_httpboot
docker volume create bifrost_mysql
docker volume create bifrost_tftpboot
docker volume create bifrost_ironic
docker volume create bifrost_ironiclib

sleep 1

docker run --rm -d --name bifrost \
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
        bifrost:${BIFROST_RELEASE:-latest}

sleep 10

docker exec -it bifrost /usr/local/bin/configure.sh

docker commit bifrost bifrost:$BIFROST_RELEASE

docker ps -q --filter "name=bifrost" | grep -q . && sleep 1 && docker stop bifrost && sleep 5 && docker rm -fv bifrost > /dev/null && sleep 5

