echo -e '{\n"ANSIBLE_MODULE_ARGS": {\n"name":"BOOTSTRAP_CEPH",\n"match_mode":"prefix"\n}\n}' |jq | python3 ansible/library/find_disks.py
