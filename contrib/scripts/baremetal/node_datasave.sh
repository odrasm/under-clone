#!/bin/bash


for i in `openstack baremetal node list --field name -f value` ; do openstack baremetal introspection data save --file introspection/$i.raw $i ; cat introspection/$i.raw | jq > introspection/$i.json ; done
