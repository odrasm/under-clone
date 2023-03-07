#!/usr/bin/python

# Copyright 2021 Ettore Simone
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This module has been relicensed from the source below:
# https://github.com/SamYaple/yaodu/blob/master/ansible/library/ceph_osd_list

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: json_merge
short_description: Merge existing JSON file with lists or dictionaries
description:
     - Dictionaries or lists will be merged into a specified JSON file.
options:
  path:
    description:
      - Path to the JSON file; this file is created if required.
    type: path
    required: true
    aliases: [ dest, file ]
  data:
    description:
      - Dictionary or list to be injected.
    required: true
    type: raw
  force:
    description:
      - Values are replaced if exists.
      - This parameter is the opposite of C(default).
    type: bool
    default: yes
  default:
    description:
      - Values inside file are preserved if exists.
      - This parameter is the opposite of C(default).
    type: bool
    default: no
  backup:
    description:
      - Create a backup file including the timestamp information so you can get
        the original file back if you somehow clobbered it incorrectly.
    type: bool
    default: no
  create:
    description:
      - If set to C(no), the module will fail if the file does not already exist.
      - By default it will create the file if it is missing.
    type: bool
    default: yes
author: Ettore Simone
'''

EXAMPLES = '''
# Consider the following JSON file:
#
# {
#   "bip" : "198.18.0.1/15",
#   "fixed-cidr" : "198.18.0.1/16"
#}

- name: Add parameters to Docker daemon.json
  become: true
  json_merge:
    path: /etc/docker/daemon.json
    data:
      registry-mirrors:
        - "http://192.168.33.1:4000"
      log-opts:
        max-size: "5m"
        max-file: "5"

# Will be changed into:
#
# {
#   "bip" : "198.18.0.1/15",
#   "fixed-cidr" : "198.18.0.1/16",
#   "registry-mirrors:": [
#     "http://192.168.33.1:4000"
#   ],
#   "log-opts": {
#     "max-size": "5m",
#     "max-file": "5"
#   }
# }
'''

import json
import yaml
import os
import tempfile
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils._text import to_bytes, to_text


def dict_merge(d1, d2):

    ret = d1.copy()

    for k, v in d2.items():
        if not ret.get(k):
            ret[k] = v
        elif k in ret and type(v) != type(ret[k]):
            raise Exception('Overlapping keys exist with different types:'
                            ' original is %s, new value is %s.'
                            % (type(ret[k]), type(v)))
        elif isinstance(ret[k], dict) and isinstance(d2[k], Mapping):
            ret[k] = dict_merge(ret[k], d2[k])
        elif isinstance(v, list):
            for list_value in v:
                if list_value not in ret[k]:
                    ret[k].append(list_value)
        else:
            ret[k] = v

    return ret


def do_json(module, filename, data, preserve, backup=False, create=True):

    diff = dict(
        before='',
        after='',
        before_header='%s (content)' % filename,
        after_header='%s (content)' % filename,
    )

    if not os.path.exists(filename):
        if not create:
            module.fail_json(rc=257, msg='Destination %s does not exist !' % filename)
        destpath = os.path.dirname(filename)
        if not os.path.exists(destpath) and not module.check_mode:
            os.makedirs(destpath)
        json_data = type(data)()
    else:
        json_file = open(filename, 'rb')
        try:
            json_data = json.load(json_file)
            # FIXME: is there anoder method to safely convert UTF-8 to string?
            json_data = yaml.safe_load(json.dumps(json_data))
        finally:
            json_file.close()

    msg = 'OK'
    if preserve:
        json_merged = dict_merge(data, json_data)
    else:
        json_merged = dict_merge(json_data, data)
    changed = json_data != json_merged

    if module._diff:
        diff['before'] = json_data
        diff['after'] = json_merged

    backup_file = None
    if changed and not module.check_mode:
        if backup:
            backup_file = module.backup_local(filename)

        try:
            tmpfd, tmpfile = tempfile.mkstemp(dir=module.tmpdir)
            f = os.fdopen(tmpfd, 'w')
            f.write(json.dumps(json_merged, indent=2) + '\n')
            f.close()
        except IOError:
            module.fail_json(msg="Unable to create temporary file %s", traceback=traceback.format_exc())

        try:
            module.atomic_move(tmpfile, filename)
        except IOError:
            module.ansible.fail_json(msg='Unable to move temporary \
                                   file %s to %s, IOError' % (tmpfile, filename), traceback=traceback.format_exc())

    return (changed, backup_file, diff, msg)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='path', required=True, aliases=['dest', 'file']),
            data=dict(type='raw', required=True),
            force=dict(type='bool', default=True),
            default=dict(type='bool', default=False),
            backup=dict(type='bool', default=False),
            create=dict(type='bool', default=True)
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ['force', 'default']
        ]
    )

    path = module.params['path']
    data = module.params['data']
    force = module.params['force']
    default = module.params['default']
    backup = module.params['backup']
    create = module.params['create']

    (changed, backup_file, diff, msg) = do_json(module, path, data, force==default, backup, create)

    if not module.check_mode and os.path.exists(path):
        file_args = module.load_file_common_arguments(module.params)
        changed = module.set_fs_attributes_if_different(file_args, changed)

    results = dict(
        changed=changed,
        diff=diff,
        msg=msg,
        path=path,
    )
    if backup_file is not None:
        results['backup_file'] = backup_file

    # Mission complete
    module.exit_json(**results)


if __name__ == '__main__':
    main()
