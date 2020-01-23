#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage Check Point Firewall (c) 2019
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: cp_mgmt_application_site
short_description: Manages application-site objects on Check Point over Web Services API
description:
  - Manages application-site objects on Check Point devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
author: "Or Soffer (@chkp-orso)"
options:
  name:
    description:
      - Object name.
    type: str
    required: True
  primary_category:
    description:
      - Each application is assigned to one primary category based on its most defining aspect.
    type: str
  url_list:
    description:
      - URLs that determine this particular application.
    type: list
  application_signature:
    description:
      - Application signature generated by <a
        href="https,//supportcenter.checkpoint.com/supportcenter/portal?eventSubmit_doGoviewsolutiondetails=&solutionid=sk103051">Signature Tool</a>.
    type: str
  additional_categories:
    description:
      - Used to configure or edit the additional categories of a custom application / site used in the Application and URL Filtering or Threat Prevention.
    type: list
  description:
    description:
      - A description for the application.
    type: str
  tags:
    description:
      - Collection of tag identifiers.
    type: list
  urls_defined_as_regular_expression:
    description:
      - States whether the URL is defined as a Regular Expression or not.
    type: bool
  color:
    description:
      - Color of the object. Should be one of existing colors.
    type: str
    choices: ['aquamarine', 'black', 'blue', 'crete blue', 'burlywood', 'cyan', 'dark green', 'khaki', 'orchid', 'dark orange', 'dark sea green',
             'pink', 'turquoise', 'dark blue', 'firebrick', 'brown', 'forest green', 'gold', 'dark gold', 'gray', 'dark gray', 'light green', 'lemon chiffon',
             'coral', 'sea green', 'sky blue', 'magenta', 'purple', 'slate blue', 'violet red', 'navy blue', 'olive', 'orange', 'red', 'sienna', 'yellow']
  comments:
    description:
      - Comments string.
    type: str
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  groups:
    description:
      - Collection of group identifiers.
    type: list
  ignore_warnings:
    description:
      - Apply changes ignoring warnings.
    type: bool
  ignore_errors:
    description:
      - Apply changes ignoring errors. You won't be able to publish such a changes. If ignore-warnings flag was omitted - warnings will also be ignored.
    type: bool

extends_documentation_fragment:
- notstdlib.moveitallout.checkpoint_objects
'''

EXAMPLES = """
- name: add-application-site
  cp_mgmt_application_site:
    additional_categories:
    - Instant Chat
    - Supports Streaming
    - New Application Site Category 1
    description: My Application Site
    name: New Application Site 1
    primary_category: Social Networking
    state: present
    url_list:
    - www.cnet.com
    - www.stackoverflow.com
    urls_defined_as_regular_expression: false

- name: set-application-site
  cp_mgmt_application_site:
    description: My New Application Site
    name: New Application Site 1
    primary_category: Instant Chat
    state: present
    urls_defined_as_regular_expression: true

- name: delete-application-site
  cp_mgmt_application_site:
    name: New Application Site 2
    state: absent
"""

RETURN = """
cp_mgmt_application_site:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible_collections.notstdlib.moveitallout.plugins.module_utils.basic import AnsibleModule
from ansible_collections.notstdlib.moveitallout.plugins.module_utils.network.checkpoint.checkpoint import checkpoint_argument_spec_for_objects, api_call


def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        primary_category=dict(type='str'),
        url_list=dict(type='list'),
        application_signature=dict(type='str'),
        additional_categories=dict(type='list'),
        description=dict(type='str'),
        tags=dict(type='list'),
        urls_defined_as_regular_expression=dict(type='bool'),
        color=dict(type='str', choices=['aquamarine', 'black', 'blue', 'crete blue', 'burlywood', 'cyan', 'dark green',
                                        'khaki', 'orchid', 'dark orange', 'dark sea green', 'pink', 'turquoise', 'dark blue', 'firebrick', 'brown',
                                        'forest green', 'gold', 'dark gold', 'gray', 'dark gray', 'light green', 'lemon chiffon', 'coral', 'sea green',
                                        'sky blue', 'magenta', 'purple', 'slate blue', 'violet red', 'navy blue', 'olive', 'orange', 'red', 'sienna',
                                        'yellow']),
        comments=dict(type='str'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        groups=dict(type='list'),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    api_call_object = 'application-site'

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
