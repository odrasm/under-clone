#!/bin/bash

/opt/stack/bifrost/bin/ansible-playbook -vvvv -i /bifrost/playbooks/inventory/target /bifrost/playbooks/install.yaml
