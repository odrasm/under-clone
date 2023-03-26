# GITHUB WORKFLOW
if [[ -n "$GITHUB_WORKSPACE" ]]; then
  echo "We are running on github workflow for tox tests"
  echo -e '{\n"ANSIBLE_MODULE_ARGS": {\n"name":"BOOTSTRAP_CEPH",\n"match_mode":"prefix"\n}\n}' | "${pythonLocation}/bin/jq" | python ansible/library/find_disks.py
else
  echo -e '{\n"ANSIBLE_MODULE_ARGS": {\n"name":"BOOTSTRAP_CEPH",\n"match_mode":"prefix"\n}\n}' | jq | python3 ansible/library/find_disks.py
fi
