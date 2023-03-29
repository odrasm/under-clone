#!/bin/bash


for i in `openstack baremetal node list --field name -f value` ; do openstack baremetal node inspect $i ; done
