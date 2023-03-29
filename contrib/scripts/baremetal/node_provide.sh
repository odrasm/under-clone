#!/bin/bash


for i in `openstack baremetal node list --field name -f value` ; do openstack baremetal node provide $i ; done
