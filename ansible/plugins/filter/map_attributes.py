# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Ettore Simone <ettore.simone@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

class FilterModule(object):

    def filters(self):
        return {'map_attributes': self.map_attributes}

    def map_attributes(self, list_of_dicts, list_of_keys):
        lll = []
        for di in list_of_dicts:
            ret = {}
        for key in list_of_keys:
            ret[key] = di[key]
        lll.append(ret)
        return lll
