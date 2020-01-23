#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
# Copyright 2019 Fortinet, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__metaclass__ = type

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: fortios_vpn_ipsec_manualkey_interface
short_description: Configure IPsec manual keys in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify vpn_ipsec feature and manualkey_interface category.
      Examples include all parameters and values need to be adjusted to datasources before usage.
      Tested with FOS v6.0.5
author:
    - Miguel Angel Munoz (@mamunozgonzalez)
    - Nicolas Thomas (@thomnico)
notes:
    - Requires fortiosapi library developed by Fortinet
    - Run as a local_action in your playbook
requirements:
    - fortiosapi>=0.9.8
options:
    host:
        description:
            - FortiOS or FortiGate IP address.
        type: str
        required: false
    username:
        description:
            - FortiOS or FortiGate username.
        type: str
        required: false
    password:
        description:
            - FortiOS or FortiGate password.
        type: str
        default: ""
    vdom:
        description:
            - Virtual domain, among those defined previously. A vdom is a
              virtual instance of the FortiGate that can be configured and
              used as a different unit.
        type: str
        default: root
    https:
        description:
            - Indicates if the requests towards FortiGate must use HTTPS protocol.
        type: bool
        default: true
    ssl_verify:
        description:
            - Ensures FortiGate certificate must be verified by a proper CA.
        type: bool
        default: true
    state:
        description:
            - Indicates whether to create or remove the object.
              This attribute was present already in previous version in a deeper level.
              It has been moved out to this outer level.
        type: str
        required: false
        choices:
            - present
            - absent
    vpn_ipsec_manualkey_interface:
        description:
            - Configure IPsec manual keys.
        default: null
        type: dict
        suboptions:
            state:
                description:
                    - B(Deprecated)
                    - Starting with Ansible 2.9 we recommend using the top-level 'state' parameter.
                    - HORIZONTALLINE
                    - Indicates whether to create or remove the object.
                type: str
                required: false
                choices:
                    - present
                    - absent
            addr_type:
                description:
                    - IP version to use for IP packets.
                type: str
                choices:
                    - 4
                    - 6
            auth_alg:
                description:
                    - Authentication algorithm. Must be the same for both ends of the tunnel.
                type: str
                choices:
                    - null
                    - md5
                    - sha1
                    - sha256
                    - sha384
                    - sha512
            auth_key:
                description:
                    - Hexadecimal authentication key in 16-digit (8-byte) segments separated by hyphens.
                type: str
            enc_alg:
                description:
                    - Encryption algorithm. Must be the same for both ends of the tunnel.
                type: str
                choices:
                    - null
                    - des
            enc_key:
                description:
                    - Hexadecimal encryption key in 16-digit (8-byte) segments separated by hyphens.
                type: str
            interface:
                description:
                    - Name of the physical, aggregate, or VLAN interface. Source system.interface.name.
                type: str
            ip_version:
                description:
                    - IP version to use for VPN interface.
                type: str
                choices:
                    - 4
                    - 6
            local_gw:
                description:
                    - IPv4 address of the local gateway's external interface.
                type: str
            local_gw6:
                description:
                    - Local IPv6 address of VPN gateway.
                type: str
            local_spi:
                description:
                    - Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.
                type: str
            name:
                description:
                    - IPsec tunnel name.
                required: true
                type: str
            remote_gw:
                description:
                    - IPv4 address of the remote gateway's external interface.
                type: str
            remote_gw6:
                description:
                    - Remote IPv6 address of VPN gateway.
                type: str
            remote_spi:
                description:
                    - Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.
                type: str
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
   ssl_verify: "False"
  tasks:
  - name: Configure IPsec manual keys.
    fortios_vpn_ipsec_manualkey_interface:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      state: "present"
      vpn_ipsec_manualkey_interface:
        addr_type: "4"
        auth_alg: "null"
        auth_key: "<your_own_value>"
        enc_alg: "null"
        enc_key: "<your_own_value>"
        interface: "<your_own_value> (source system.interface.name)"
        ip_version: "4"
        local_gw: "<your_own_value>"
        local_gw6: "<your_own_value>"
        local_spi: "<your_own_value>"
        name: "default_name_13"
        remote_gw: "<your_own_value>"
        remote_gw6: "<your_own_value>"
        remote_spi: "<your_own_value>"
'''

RETURN = '''
build:
  description: Build number of the fortigate image
  returned: always
  type: str
  sample: '1547'
http_method:
  description: Last method used to provision the content into FortiGate
  returned: always
  type: str
  sample: 'PUT'
http_status:
  description: Last result given by FortiGate on last operation applied
  returned: always
  type: str
  sample: "200"
mkey:
  description: Master key (id) used in the last call to FortiGate
  returned: success
  type: str
  sample: "id"
name:
  description: Name of the table used to fulfill the request
  returned: always
  type: str
  sample: "urlfilter"
path:
  description: Path of the table used to fulfill the request
  returned: always
  type: str
  sample: "webfilter"
revision:
  description: Internal revision number
  returned: always
  type: str
  sample: "17.0.2.10658"
serial:
  description: Serial number of the unit
  returned: always
  type: str
  sample: "FGVMEVYYQT3AB5352"
status:
  description: Indication of the operation's result
  returned: always
  type: str
  sample: "success"
vdom:
  description: Virtual domain used
  returned: always
  type: str
  sample: "root"
version:
  description: Version of the FortiGate
  returned: always
  type: str
  sample: "v5.6.3"

'''

from ansible_collections.notstdlib.moveitallout.plugins.module_utils.basic import AnsibleModule
from ansible_collections.notstdlib.moveitallout.plugins.module_utils.connection import Connection
from ansible_collections.notstdlib.moveitallout.plugins.module_utils.network.fortios.fortios import FortiOSHandler
from ansible_collections.notstdlib.moveitallout.plugins.module_utils.network.fortimanager.common import FAIL_SOCKET_MSG


def login(data, fos):
    host = data['host']
    username = data['username']
    password = data['password']
    ssl_verify = data['ssl_verify']

    fos.debug('on')
    if 'https' in data and not data['https']:
        fos.https('off')
    else:
        fos.https('on')

    fos.login(host, username, password, verify=ssl_verify)


def filter_vpn_ipsec_manualkey_interface_data(json):
    option_list = ['addr_type', 'auth_alg', 'auth_key',
                   'enc_alg', 'enc_key', 'interface',
                   'ip_version', 'local_gw', 'local_gw6',
                   'local_spi', 'name', 'remote_gw',
                   'remote_gw6', 'remote_spi']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def underscore_to_hyphen(data):
    if isinstance(data, list):
        for i, elem in enumerate(data):
            data[i] = underscore_to_hyphen(elem)
    elif isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k.replace('_', '-')] = underscore_to_hyphen(v)
        data = new_data

    return data


def vpn_ipsec_manualkey_interface(data, fos):
    vdom = data['vdom']
    if 'state' in data and data['state']:
        state = data['state']
    elif 'state' in data['vpn_ipsec_manualkey_interface'] and data['vpn_ipsec_manualkey_interface']:
        state = data['vpn_ipsec_manualkey_interface']['state']
    else:
        state = True
    vpn_ipsec_manualkey_interface_data = data['vpn_ipsec_manualkey_interface']
    filtered_data = underscore_to_hyphen(filter_vpn_ipsec_manualkey_interface_data(vpn_ipsec_manualkey_interface_data))

    if state == "present":
        return fos.set('vpn.ipsec',
                       'manualkey-interface',
                       data=filtered_data,
                       vdom=vdom)

    elif state == "absent":
        return fos.delete('vpn.ipsec',
                          'manualkey-interface',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_vpn_ipsec(data, fos):

    if data['vpn_ipsec_manualkey_interface']:
        resp = vpn_ipsec_manualkey_interface(data, fos)

    return not is_successful_status(resp), \
        resp['status'] == "success", \
        resp


def main():
    fields = {
        "host": {"required": False, "type": "str"},
        "username": {"required": False, "type": "str"},
        "password": {"required": False, "type": "str", "default": "", "no_log": True},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "https": {"required": False, "type": "bool", "default": True},
        "ssl_verify": {"required": False, "type": "bool", "default": True},
        "state": {"required": False, "type": "str",
                  "choices": ["present", "absent"]},
        "vpn_ipsec_manualkey_interface": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "state": {"required": False, "type": "str",
                          "choices": ["present", "absent"]},
                "addr_type": {"required": False, "type": "str",
                              "choices": ["4", "6"]},
                "auth_alg": {"required": False, "type": "str",
                             "choices": ["null", "md5", "sha1",
                                         "sha256", "sha384", "sha512"]},
                "auth_key": {"required": False, "type": "str"},
                "enc_alg": {"required": False, "type": "str",
                            "choices": ["null", "des"]},
                "enc_key": {"required": False, "type": "str"},
                "interface": {"required": False, "type": "str"},
                "ip_version": {"required": False, "type": "str",
                               "choices": ["4", "6"]},
                "local_gw": {"required": False, "type": "str"},
                "local_gw6": {"required": False, "type": "str"},
                "local_spi": {"required": False, "type": "str"},
                "name": {"required": True, "type": "str"},
                "remote_gw": {"required": False, "type": "str"},
                "remote_gw6": {"required": False, "type": "str"},
                "remote_spi": {"required": False, "type": "str"}

            }
        }
    }

    module = AnsibleModule(argument_spec=fields,
                           supports_check_mode=False)

    # legacy_mode refers to using fortiosapi instead of HTTPAPI
    legacy_mode = 'host' in module.params and module.params['host'] is not None and \
                  'username' in module.params and module.params['username'] is not None and \
                  'password' in module.params and module.params['password'] is not None

    if not legacy_mode:
        if module._socket_path:
            connection = Connection(module._socket_path)
            fos = FortiOSHandler(connection)

            is_error, has_changed, result = fortios_vpn_ipsec(module.params, fos)
        else:
            module.fail_json(**FAIL_SOCKET_MSG)
    else:
        try:
            from fortiosapi import FortiOSAPI
        except ImportError:
            module.fail_json(msg="fortiosapi module is required")

        fos = FortiOSAPI()

        login(module.params, fos)
        is_error, has_changed, result = fortios_vpn_ipsec(module.params, fos)
        fos.logout()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
