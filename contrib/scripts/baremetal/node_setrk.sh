#!/bin/bash

for i in `openstack baremetal node list --fields name -f value` ; do
	IP=`openstack baremetal node show $i --fields driver_info -f json | jq '.[] .ipmi_address' | sed -e 's/"//g'` ;
	RK=`ipmitool -H $IP -U ADMIN -P ADMIN -I lanplus fru|grep 'Product Serial' | awk '{print$4}'` ;
	echo $i ;
	echo $IP ;
	echo $RK ;
	openstack baremetal node set --property E4RK="$RK" $i ;
done
