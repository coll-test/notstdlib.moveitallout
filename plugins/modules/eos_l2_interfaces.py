#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

##############################################
#                 WARNING                    #
##############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
##############################################

"""
The module file for eos_l2_interfaces
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'network'
}

DOCUMENTATION = '''
---
module: eos_l2_interfaces
short_description: Manages Layer-2 interface attributes of Arista EOS devices
description: This module provides declarative management of Layer-2 interface on Arista EOS devices.
author: Nathaniel Case (@qalthos)
notes:
- Tested against Arista EOS 4.20.10M
- This module works with connection C(network_cli). See the
  L(EOS Platform Options,../network/user_guide/platform_eos.html).
options:
  config:
    description: A dictionary of Layer-2 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of interface, e.g. Ethernet1.
        type: str
        required: True
      access:
        description:
        - Switchport mode access command to configure the interface as a layer 2 access.
        type: dict
        suboptions:
          vlan:
            description:
            - Configure given VLAN in access port. It's used as the access VLAN ID.
            type: int
      trunk:
        description:
        - Switchport mode trunk command to configure the interface as a Layer 2 trunk.
        type: dict
        suboptions:
          native_vlan:
            description:
            - Native VLAN to be configured in trunk port. It is used as the trunk native VLAN ID.
            type: int
          trunk_allowed_vlans:
            description:
            - List of allowed VLANs in a given trunk port. These are the only VLANs that will be
              configured on the trunk.
            type: list
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    default: merged
    description:
    - The state of the configuration after module completion
    type: str
'''

EXAMPLES = """
---

# Using merged

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    switchport access vlan 20
# !
# interface Ethernet2
#    switchport trunk native vlan 20
#    switchport mode trunk
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
# !

- name: Merge provided configuration with device configuration.
  eos_l2_interfaces:
    config:
      - name: Ethernet1
        trunk:
          native_vlan: 10
      - name: Ethernet2
        access:
          vlan: 30
    state: merged

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    switchport trunk native vlan 10
#    switchport mode trunk
# !
# interface Ethernet2
#    switchport access vlan 30
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
# !

# Using replaced

# Before state:
# -------------
#
# veos2#show running-config | s int
# interface Ethernet1
#    switchport access vlan 20
# !
# interface Ethernet2
#    switchport trunk native vlan 20
#    switchport mode trunk
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
# !

- name: Replace device configuration of specified L2 interfaces with provided configuration.
  eos_l2_interfaces:
    config:
      - name: Ethernet1
        trunk:
          native_vlan: 20
          trunk_vlans: 5-10, 15
    state: replaced

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    switchport trunk native vlan 20
#    switchport trunk allowed vlan 5-10,15
#    switchport mode trunk
# !
# interface Ethernet2
#    switchport trunk native vlan 20
#    switchport mode trunk
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
# !

# Using overridden

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    switchport access vlan 20
# !
# interface Ethernet2
#    switchport trunk native vlan 20
#    switchport mode trunk
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
# !

- name: Override device configuration of all L2 interfaces on device with provided configuration.
  eos_l2_interfaces:
    config:
      - name: Ethernet2
        access:
          vlan: 30
    state: overridden

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
# !
# interface Ethernet2
#    switchport access vlan 30
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
# !

# Using deleted

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    switchport access vlan 20
# !
# interface Ethernet2
#    switchport trunk native vlan 20
#    switchport mode trunk
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
# !

- name: Delete EOS L2 interfaces as in given arguments.
  eos_l2_interfaces:
    config:
      - name: Ethernet1
      - name: Ethernet2
    state: deleted

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
# !
# interface Ethernet2
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config
"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['interface Ethernet2', 'switchport access vlan 20']
"""


from ansible_collections.notstdlib.moveitallout.plugins.module_utils.basic import AnsibleModule
from ansible_collections.notstdlib.moveitallout.plugins.module_utils.network.eos.argspec.l2_interfaces.l2_interfaces import L2_interfacesArgs
from ansible_collections.notstdlib.moveitallout.plugins.module_utils.network.eos.config.l2_interfaces.l2_interfaces import L2_interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=L2_interfacesArgs.argument_spec,
                           supports_check_mode=True)

    result = L2_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
