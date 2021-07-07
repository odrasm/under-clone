#!/bin/bash

source versions.sh

read -r -p "Are you sure? This Action is bad like docker system prune [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	docker volume list | awk '{print$2}' |grep bifrost_| xargs -n1 docker volume rm
	docker rmi bifrost:$BIFROST_TAG
	docker system prune -f --volumes
else
	exit 0
fi

