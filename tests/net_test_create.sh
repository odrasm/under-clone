#!/bin/bash

ip link add public type dummy
ip link add api type dummy
ip link add neutron type dummy
ip addr add 192.168.0.1/24 dev public
ip addr add 192.168.1.1/24 dev api
ip link set public up
ip link set api up
ip link set neutron up
