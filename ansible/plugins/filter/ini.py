# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Ettore Simone <ettore.simone@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

def ini_dict_flatten(arg):
    ret = []
    for section, subdict in arg.items():
        for option, value in subdict.items():
            ret.append(dict(section=section,
                            option=option,
                            value=value))
    return ret

class FilterModule(object):
    ''' Ansible INI filters '''

    def filters(self):
        filters = {
            'ini_dict_flatten': ini_dict_flatten,
        }
        return filters

