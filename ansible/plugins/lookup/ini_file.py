# (c) 2015, Yannig Perre <yannig.perre(at)gmail.com>
# (c) 2017 Ansible Project
# (c) 2021, Ettore Simone <ettore.simone(at)gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re
from io import StringIO

from ansible.errors import AnsibleError, AnsibleAssertionError
from ansible.module_utils.six.moves import configparser
from ansible.module_utils.six import PY3, string_types
from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.lookup import LookupBase

# Load DEFAULT as a normal section
configparser.DEFAULTSECT = None


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        cp = configparser.ConfigParser()

        ret = {}
        for term in terms:
            path = self.find_file_in_search_path(variables, 'files', term)

            with open(to_bytes(path), 'rb') as f:
                try:
                    cfg_text = to_text(f.read(), errors='surrogate_or_strict')
                except UnicodeError as e:
                    raise AnsibleOptionsError("Error reading config file(%s) because the config file was not utf8 encoded: %s" % (path, to_native(e)))
            try:
                if PY3:
                    cp.read_string(cfg_text)
                else:
                    cfg_file = StringIO(cfg_text)
                    cp.readfp(cfg_file)
            except configparser.Error as e:
                raise AnsibleOptionsError("Error reading config file (%s): %s" % (cfile, to_native(e)))

            for section in cp.sections():
                ret[section] = {}
                for option, value in cp.items(section):
                    ret[section].update({option: value})
        return [ret]
