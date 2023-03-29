#!/bin/bash

pip install -r /workspace/underground/requirements.txt
python -m pip install --upgrade --no-deps --force-reinstall /workspace/underground
underground init aio zed -m minimal --inventory /workspace/underground/ansible/inventory/aio --configdir /workspace/etc/underground
underground configure -e "@/workspace/underground/tests/test_vars.yml" --inventory /workspace/underground/ansible/inventory/aio --configdir /workspace/etc/underground
underground build -t dib -e underground_baremetal_image="ipa" --inventory /workspace/underground/ansible/inventory/aio --configdir /workspace/etc/underground build
sed -i '37,38 s/^/#/' /home/vscode/.ansible/collections/ansible_collections/openstack/kolla/roles/baremetal/tasks/install.yml
underground bootstrap --inventory /workspace/underground/ansible/inventory/aio --configdir /workspace/etc/underground -e customize_etc_hosts=false
