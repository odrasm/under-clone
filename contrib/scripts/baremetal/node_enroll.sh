#!/bin/bash

NODE=$1
IPMI=$2
MACADDRESS=$3

openstack baremetal node create --driver ipmi --name $NODE
openstack baremetal node set $NODE --resource-class BAREMETAL
openstack baremetal node set $NODE --driver ipmi --driver-info ipmi_address=$IPMI --driver-info ipmi_username="ADMIN" --driver-info ipmi_password="ADMIN"
openstack baremetal node set $NODE --driver-info deploy_kernel="ff472f11-91fd-4bad-9223-a9821fa52d09" --driver-info deploy_ramdisk="14e22638-9c85-46f8-ac3d-5ce49e22c1c6"
openstack baremetal node set $NODE --property capabilities=boot_mode:bios
UUID=`openstack baremetal node show $NODE --fields uuid -f value`
openstack baremetal port create --node $UUID --pxe-enabled true $MACADDRESS
openstack baremetal node manage $NODE
