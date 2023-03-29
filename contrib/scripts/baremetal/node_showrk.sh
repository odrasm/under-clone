#!/bin/bash

for i in `openstack baremetal node list --fields name -f value` ; do openstack baremetal node show $i --fields name --fields properties ; done
