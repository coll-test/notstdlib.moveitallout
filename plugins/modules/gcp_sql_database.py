#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_sql_database
description:
- Represents a SQL database inside the Cloud SQL instance, hosted in Google's cloud.
short_description: Creates a GCP Database
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  state:
    description:
    - Whether the given object should exist in GCP
    choices:
    - present
    - absent
    default: present
    type: str
  charset:
    description:
    - The charset value. See MySQL's [Supported Character Sets and Collations](U(https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html))
      and Postgres' [Character Set Support](U(https://www.postgresql.org/docs/9.6/static/multibyte.html))
      for more details and supported values. Postgres databases only support a value
      of `UTF8` at creation time.
    required: false
    type: str
  collation:
    description:
    - The collation value. See MySQL's [Supported Character Sets and Collations](U(https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html))
      and Postgres' [Collation Support](U(https://www.postgresql.org/docs/9.6/static/collation.html))
      for more details and supported values. Postgres databases only support a value
      of `en_US.UTF8` at creation time.
    required: false
    type: str
  name:
    description:
    - The name of the database in the Cloud SQL instance.
    - This does not include the project ID or instance name.
    required: true
    type: str
  instance:
    description:
    - The name of the Cloud SQL instance. This does not include the project ID.
    required: true
    type: str
  project:
    description:
    - The Google Cloud Platform project to use.
    type: str
  auth_kind:
    description:
    - The type of credential used.
    type: str
    required: true
    choices:
    - application
    - machineaccount
    - serviceaccount
  service_account_contents:
    description:
    - The contents of a Service Account JSON file, either in a dictionary or as a
      JSON string that represents it.
    type: jsonarg
  service_account_file:
    description:
    - The path of a Service Account JSON file if serviceaccount is selected as type.
    type: path
  service_account_email:
    description:
    - An optional service account email address if machineaccount is selected and
      the user does not wish to use the default email.
    type: str
  scopes:
    description:
    - Array of scopes to be used
    type: list
  env_type:
    description:
    - Specifies which Ansible environment you're running this module within.
    - This should not be set unless you know what you're doing.
    - This only alters the User Agent string for any API requests.
    type: str
'''

EXAMPLES = '''
- name: create a instance
  gcp_sql_instance:
    name: "{{resource_name}}-3"
    settings:
      ip_configuration:
        authorized_networks:
        - name: google dns server
          value: 8.8.8.8/32
      tier: db-n1-standard-1
    region: us-central1
    project: "{{ gcp_project }}"
    auth_kind: "{{ gcp_cred_kind }}"
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: instance

- name: create a database
  gcp_sql_database:
    name: test_object
    charset: utf8
    instance: "{{ instance.name }}"
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
charset:
  description:
  - The charset value. See MySQL's [Supported Character Sets and Collations](U(https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html))
    and Postgres' [Character Set Support](U(https://www.postgresql.org/docs/9.6/static/multibyte.html))
    for more details and supported values. Postgres databases only support a value
    of `UTF8` at creation time.
  returned: success
  type: str
collation:
  description:
  - The collation value. See MySQL's [Supported Character Sets and Collations](U(https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html))
    and Postgres' [Collation Support](U(https://www.postgresql.org/docs/9.6/static/collation.html))
    for more details and supported values. Postgres databases only support a value
    of `en_US.UTF8` at creation time.
  returned: success
  type: str
name:
  description:
  - The name of the database in the Cloud SQL instance.
  - This does not include the project ID or instance name.
  returned: success
  type: str
instance:
  description:
  - The name of the Cloud SQL instance. This does not include the project ID.
  returned: success
  type: str
'''

################################################################################
# Imports
################################################################################

from ansible_collections.notstdlib.moveitallout.plugins.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, replace_resource_dict
import json
import time

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            charset=dict(type='str'),
            collation=dict(type='str'),
            name=dict(required=True, type='str'),
            instance=dict(required=True, type='str'),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/sqlservice.admin']

    state = module.params['state']
    kind = 'sql#database'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), kind)
                fetch = fetch_resource(module, self_link(module), kind)
                changed = True
        else:
            delete(module, self_link(module), kind)
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module), kind)
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link, kind):
    auth = GcpSession(module, 'sql')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link, kind):
    module.fail_json(msg="SQL objects can't be updated to ensure data safety")


def delete(module, link, kind):
    auth = GcpSession(module, 'sql')
    return wait_for_operation(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'kind': 'sql#database',
        u'instance': module.params.get('instance'),
        u'charset': module.params.get('charset'),
        u'collation': module.params.get('collation'),
        u'name': module.params.get('name'),
    }
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind, allow_not_found=True):
    auth = GcpSession(module, 'sql')
    return return_if_object(module, auth.get(link), kind, allow_not_found)


def self_link(module):
    return "https://www.googleapis.com/sql/v1beta4/projects/{project}/instances/{instance}/databases/{name}".format(**module.params)


def collection(module):
    return "https://www.googleapis.com/sql/v1beta4/projects/{project}/instances/{instance}/databases".format(**module.params)


def return_if_object(module, response, kind, allow_not_found=False):
    # If not found, return nothing.
    if allow_not_found and response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    # SQL only: return on 403 if not exist
    if allow_not_found and response.status_code == 403:
        return None

    try:
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {u'charset': response.get(u'charset'), u'collation': response.get(u'collation'), u'name': module.params.get('name')}


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://www.googleapis.com/sql/v1beta4/projects/{project}/operations/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response, 'sql#operation')
    if op_result is None:
        return {}
    status = navigate_hash(op_result, ['status'])
    wait_done = wait_for_completion(status, op_result, module)
    return fetch_resource(module, navigate_hash(wait_done, ['targetLink']), 'sql#database')


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while status != 'DONE':
        raise_if_errors(op_result, ['error', 'errors'], module)
        time.sleep(1.0)
        op_result = fetch_resource(module, op_uri, 'sql#operation', False)
        status = navigate_hash(op_result, ['status'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


if __name__ == '__main__':
    main()
