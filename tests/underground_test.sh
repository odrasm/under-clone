#!/bin/bash

python -m pip install --upgrade --no-deps --force-reinstall /workspace/underground
underground init aio zed -m minimal --inventory /workspace/underground/ansible/inventory/aio --configdir /workspace/etc/underground
underground configure -e "@/workspace/underground/tests/test_vars.yml" --inventory /workspace/underground/ansible/inventory/aio --configdir /workspace/etc/underground
