#
# (c) 2018 Extreme Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible_collections.notstdlib.moveitallout.plugins.action.network import ActionModule as ActionNetworkModule

PRIVATE_KEYS_RE = re.compile('__.+__')


class ActionModule(ActionNetworkModule):

    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split('.')[-1]
        self._config_module = True if module_name == 'slxos_config' else False
        persistent_connection = self._play_context.connection.split('.')[-1]

        if persistent_connection not in ('network_cli'):
            return {'failed': True, 'msg': 'Connection type %s is not valid for this module' % self._play_context.connection}
        return super(ActionModule, self).run(task_vars=task_vars)
