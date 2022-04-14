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
module: yaml_merge
short_description: Merge existing YAML file with lists or dictionaries
description:
     - Dictionaries or lists will be merged into a specified YAML file.
options:
  path:
    description:
      - Path to the YAML file; this file is created if required.
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
# Consider the following YAML file:
#
# people:
# - name: Ettore
#   surname: Simone
#   phone: +39 555 11.22.33
# administrator:
#   name: Ettore

- name: Add John Doe to the people list
  yaml_merge:
    path: /path/to/file.yml
    dict:
      people:
      - name: John
        surname: Doe
        address: Unknown

- name Replace administrator name
  yaml_merge:
    path: /path/to/file.yml
    dict:
      administrator:
        name: John
'''

import yaml

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


def do_yaml(module, filename, data, preserve, backup=False, create=True):

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
        yaml_data = type(data)()
    else:
        yaml_file = open(filename, 'r')
        try:
            yaml_data = yaml.safe_load(yaml_file)
        finally:
            yaml_file.close()

    if preserve:
        yaml_merged = dict_merge(data, yaml_data)
    else:
        yaml_merged = dict_merge(yaml_data, data)
    changed = yaml_data != yaml_merged

    if module._diff:
        diff['before'] = yaml_data
        diff['after'] = yaml_merged

    backup_file = None
    if changed and not module.check_mode:
        if backup:
            backup_file = module.backup_local(filename)

        try:
            tmpfd, tmpfile = tempfile.mkstemp(dir=module.tmpdir)
            f = os.fdopen(tmpfd, 'w')
            f.write(yaml.dump(yaml_merged, default_flow_style=False))
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
    data = data_dict if data_dict else data_list

    (changed, backup_file, diff, msg) = do_yaml(module, path, data, force==default, backup, create)

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
