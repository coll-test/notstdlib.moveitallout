#!/usr/bin/python

# Copyright: (c) 2017, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
module: vcenter_license
short_description: Manage VMware vCenter license keys
description:
- Add and delete vCenter, ESXi server license keys.
author:
- Dag Wieers (@dagwieers)
requirements:
- pyVmomi
options:
  labels:
    description:
    - The optional labels of the license key to manage in vSphere vCenter.
    - This is dictionary with key/value pair.
    default: {
        'source': 'ansible'
    }
    type: dict
  license:
    description:
    - The license key to manage in vSphere vCenter.
    required: yes
    type: str
  state:
    description:
    -  Whether to add (C(present)) or remove (C(absent)) the license key.
    choices: [absent, present]
    default: present
    type: str
  esxi_hostname:
    description:
    - The hostname of the ESXi server to which the specified license will be assigned.
    - This parameter is optional.
    type: str
  datacenter:
    description:
    - The datacenter name to use for the operation.
    type: str
  cluster_name:
    description:
    - Name of the cluster to apply vSAN license.
    type: str
notes:
- This module will also auto-assign the current vCenter to the license key
  if the product matches the license key, and vCenter us currently assigned
  an evaluation license only.
- The evaluation license (00000-00000-00000-00000-00000) is not listed
  when unused.
- If C(esxi_hostname) is specified, then will assign the C(license) key to
  the ESXi host.

extends_documentation_fragment:
- notstdlib.moveitallout.vmware.vcenter_documentation
'''

EXAMPLES = r'''
- name: Add a new vCenter license
  vcenter_license:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    license: f600d-21ae3-5592b-249e0-cc341
    state: present
  delegate_to: localhost

- name: Remove an (unused) vCenter license
  vcenter_license:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    license: f600d-21ae3-5592b-249e0-cc341
    state: absent
  delegate_to: localhost

- name: Add ESXi license and assign to the ESXi host
  vcenter_license:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    esxi_hostname: '{{ esxi_hostname }}'
    license: f600d-21ae3-5592b-249e0-dd502
    state: present
  delegate_to: localhost

- name: Add vSAN license and assign to the given cluster
  vcenter_license:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    datacenter: '{{ datacenter_name }}'
    cluster_name: '{{ cluster_name }}'
    license: f600d-21ae3-5592b-249e0-dd502
    state: present
  delegate_to: localhost
'''

RETURN = r'''
licenses:
    description: list of license keys after module executed
    returned: always
    type: list
    sample:
    - f600d-21ae3-5592b-249e0-cc341
    - 143cc-0e942-b2955-3ea12-d006f
'''

try:
    from pyVmomi import vim
except ImportError:
    pass

from ansible_collections.notstdlib.moveitallout.plugins.module_utils.basic import AnsibleModule
from ansible_collections.notstdlib.moveitallout.plugins.module_utils._text import to_native
from ansible_collections.notstdlib.moveitallout.plugins.module_utils.vmware import PyVmomi, vmware_argument_spec, find_hostsystem_by_name


class VcenterLicenseMgr(PyVmomi):
    def __init__(self, module):
        super(VcenterLicenseMgr, self).__init__(module)

    def find_key(self, licenses, license):
        for item in licenses:
            if item.licenseKey == license:
                return item
        return None

    def list_keys(self, licenses):
        keys = []
        for item in licenses:
            # Filter out evaluation license key
            if item.used is None:
                continue
            keys.append(item.licenseKey)
        return keys


def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(
        labels=dict(type='dict', default=dict(source='ansible')),
        license=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['absent', 'present']),
        esxi_hostname=dict(type='str'),
        datacenter=dict(type='str'),
        cluster_name=dict(type='str'),
    ))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    license = module.params['license']
    state = module.params['state']

    # FIXME: This does not seem to work on vCenter v6.0
    labels = []
    for k in module.params['labels']:
        kv = vim.KeyValue()
        kv.key = k
        kv.value = module.params['labels'][k]
        labels.append(kv)

    result = dict(
        changed=False,
        diff=dict(),
    )

    pyv = VcenterLicenseMgr(module)
    if not pyv.is_vcenter():
        module.fail_json(msg="vcenter_license is meant for vCenter, hostname %s "
                             "is not vCenter server." % module.params.get('hostname'))

    lm = pyv.content.licenseManager

    result['licenses'] = pyv.list_keys(lm.licenses)
    if module._diff:
        result['diff']['before'] = '\n'.join(result['licenses']) + '\n'

    if state == 'present':
        if license not in result['licenses']:
            result['changed'] = True
            if module.check_mode:
                result['licenses'].append(license)
            else:
                lm.AddLicense(license, labels)

        key = pyv.find_key(lm.licenses, license)
        if key is not None:
            lam = lm.licenseAssignmentManager
            assigned_license = None
            datacenter = module.params['datacenter']
            datacenter_obj = None
            if datacenter:
                datacenter_obj = pyv.find_datacenter_by_name(datacenter)
                if not datacenter_obj:
                    module.fail_json(msg="Unable to find the datacenter %(datacenter)s" % module.params)

            cluster = module.params['cluster_name']
            if cluster:
                cluster_obj = pyv.find_cluster_by_name(cluster_name=cluster, datacenter_name=datacenter_obj)
                if not cluster_obj:
                    msg = "Unable to find the cluster %(cluster_name)s"
                    if datacenter:
                        msg += " in datacenter %(datacenter)s"
                    module.fail_json(msg=msg % module.params)
                entityId = cluster_obj._moId
            # assign to current vCenter, if esxi_hostname is not specified
            elif module.params['esxi_hostname'] is None:
                entityId = pyv.content.about.instanceUuid
                # if key name not contain "VMware vCenter Server"
                if pyv.content.about.name not in key.name:
                    module.warn('License key "%s" (%s) is not suitable for "%s"' % (license, key.name, pyv.content.about.name))
            # assign to ESXi server
            else:
                esxi_host = find_hostsystem_by_name(pyv.content, module.params['esxi_hostname'])
                if esxi_host is None:
                    module.fail_json(msg='Cannot find the specified ESXi host "%s".' % module.params['esxi_hostname'])
                entityId = esxi_host._moId
                # e.g., key.editionKey is "esx.enterprisePlus.cpuPackage", not sure all keys are in this format
                if 'esx' not in key.editionKey:
                    module.warn('License key "%s" edition "%s" is not suitable for ESXi server' % (license, key.editionKey))

            try:
                assigned_license = lam.QueryAssignedLicenses(entityId=entityId)
            except Exception as e:
                module.fail_json(msg='Could not query vCenter "%s" assigned license info due to %s.' % (entityId, to_native(e)))

            if not assigned_license or (len(assigned_license) != 0 and assigned_license[0].assignedLicense.licenseKey != license):
                try:
                    lam.UpdateAssignedLicense(entity=entityId, licenseKey=license)
                except Exception:
                    module.fail_json(msg='Could not assign "%s" (%s) to vCenter.' % (license, key.name))
                result['changed'] = True
            result['licenses'] = pyv.list_keys(lm.licenses)
        else:
            module.fail_json(msg='License "%s" is not existing or can not be added' % license)
        if module._diff:
            result['diff']['after'] = '\n'.join(result['licenses']) + '\n'

    elif state == 'absent' and license in result['licenses']:

        # Check if key is in use
        key = pyv.find_key(lm.licenses, license)
        if key.used > 0:
            module.fail_json(msg='Cannot remove key "%s", still in use %s time(s).' % (license, key.used))

        result['changed'] = True
        if module.check_mode:
            result['licenses'].remove(license)
        else:
            lm.RemoveLicense(license)
            result['licenses'] = pyv.list_keys(lm.licenses)
        if module._diff:
            result['diff']['after'] = '\n'.join(result['licenses']) + '\n'

    module.exit_json(**result)


if __name__ == '__main__':
    main()
