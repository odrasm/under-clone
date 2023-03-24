#!/usr/bin/python

# Copyright 2015 Sam Yaple
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

# import json

import pyudev
import psutil
import re
import subprocess  # nosec

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: find_disks
short_description: Return list of devices containing a specfied name or label
description:
     - This will return a list of all devices with either GPT partition name
       or filesystem label of the name specified.
options:
  match_mode:
    description:
      - Label match mode, either strict, prefix or substr
    default: 'strict'
    required: False
    choices: [ "strict", "prefix", "substr" ]
    type: str
  name:
    description:
      - Partition name or filesystem label
    required: True
    type: str
    aliases: [ 'partition_name' ]
  use_udev:
    description:
      - When True, use Linux udev to read disk info such as partition labels,
        uuid, etc.  Some older host operating systems have issues using udev to
        get the info this module needs. Set to False to fall back to more low
        level commands such as blkid to retrieve this information. Most users
        should not need to change this.
    default: True
    required: False
    type: bool
author: Ettore Simone
'''

EXAMPLES = '''
- hosts: osds
  tasks:
    - name: Return all devices with name starting with BOOTSTRAP_CEPH_
      find_disks:
          name: 'BOOTSTRAP_CEPH_'
          match_mode: 'prefix'
      register: disk_list
- hosts: miniosrv
  tasks:
    - name: Return all devices with name starting with BOOTSTRAP_MINIO
      find_disks:
          name: 'BOOTSTRAP_MINIO'
          match_mode: 'prefix'
      register: disk_list
'''


PREFERRED_DEVICE_LINK_ORDER = [
    '/dev/disk/by-uuid',
    '/dev/disk/by-partuuid',
    '/dev/disk/by-parttypeuuid',
    '/dev/disk/by-label',
    '/dev/disk/by-partlabel'
]


def get_id_part_entry_name(dev, use_udev):
    if use_udev:
        dev_name = dev.get('ID_PART_ENTRY_NAME', '')
    else:
        part = re.sub(r'.*[^\d]', '', dev.device_node)
        parent = dev.find_parent('block').device_node
        # NOTE(Mech422): Need to use -i as -p truncates the partition name
        out = subprocess.Popen(['/usr/sbin/sgdisk', '-i', part,  # nosec
                                parent],
                               stdout=subprocess.PIPE).communicate()
        match = re.search(r'Partition name: \'(\w+)\'', out[0])
        if match:
            dev_name = match.group(1)
        else:
            dev_name = ''
    return dev_name


def get_id_fs_uuid(dev, use_udev):
    if use_udev:
        id_fs_uuid = dev.get('ID_FS_UUID', '')
    else:
        out = subprocess.Popen(['/usr/sbin/blkid', '-o', 'export',  # nosec
                                dev.device_node],
                               stdout=subprocess.PIPE).communicate()
        match = re.search(r'\nUUID=([\w-]+)', out[0])
        if match:
            id_fs_uuid = match.group(1)
        else:
            id_fs_uuid = ''
    return id_fs_uuid


def is_dev_matched_by_name(dev, name, mode, use_udev):
    if dev.get('DEVTYPE', '') == 'partition':
        dev_name = get_id_part_entry_name(dev, use_udev)
    else:
        dev_name = dev.get('ID_FS_LABEL', '')

    if mode == 'strict':
        return dev_name == name
    elif mode == 'prefix':
        return dev_name.startswith(name)
    elif mode == 'substr':
        return name in dev_name
    else:
        return False


def find_disk(ct, name, match_mode, use_udev):
    for dev in ct.list_devices(subsystem='block'):
        if is_dev_matched_by_name(dev, name, match_mode, use_udev):
            yield dev


def extract_disk_info(ct, dev, name, use_udev):
    if not dev:
        return
    kwargs = dict()
    kwargs['fs_uuid'] = get_id_fs_uuid(dev, use_udev)
    kwargs['fs_label'] = dev.get('ID_FS_LABEL', '')
    if dev.get('DEVTYPE', '') == 'partition':
        kwargs['partition_label'] = get_id_part_entry_name(dev, use_udev)
        kwargs['device'] = dev.find_parent('block').device_node
        kwargs['partition'] = dev.device_node
        kwargs['partition_num'] = re.sub(r'.*[^\d]', '', dev.device_node)
        for mount in psutil.disk_partitions():
            if mount.device == kwargs['partition']:
                kwargs['mount_point'] = mount.mountpoint
    else:
        kwargs['device'] = dev.device_node
        for mount in psutil.disk_partitions():
            if mount.device == kwargs['device']:
                kwargs['mount_point'] = mount.mountpoint
    yield kwargs


def main():
    argument_spec = dict(
        match_mode=dict(required=False, choices=['strict', 'prefix', 'substr'],
                        default='strict'),
        name=dict(aliases=['partition_name'], required=True, type='str'),
        use_udev=dict(required=False, default=True, type='bool')
    )
    module = AnsibleModule(argument_spec)
    match_mode = module.params.get('match_mode')
    name = module.params.get('name')
    use_udev = module.params.get('use_udev')

    try:
        ret = list()
        ct = pyudev.Context()
        for dev in find_disk(ct, name, match_mode, use_udev):
            for info in extract_disk_info(ct, dev, name, use_udev):
                if info:
                    ret.append(info)

        module.exit_json(disks=ret)
    except Exception as e:
        module.exit_json(failed=True, msg=repr(e))


if __name__ == '__main__':
    main()
