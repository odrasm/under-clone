#!/bin/bash

/opt/stack/bifrost/bin/ansible-playbook -vvvv -i /bifrost/playbooks/inventory/bifrost_inventory.py /bifrost/playbooks/enroll-dynamic.yaml --connection=local