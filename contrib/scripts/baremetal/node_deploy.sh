#!/bin/bash

NODE=$1
IP=$2

openstack baremetal node provide $NODE
sleep 20
openstack server create --config-drive True --image Rocky-8-Base --flavor baremetal-bios --nic net-id=cluster,v4-fixed-ip=$IP --key-name e4user $NODE
