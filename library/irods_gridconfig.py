#!/usr/bin/python
# Copyright (c) 2021-2024 Utrecht University
# GNU General Public License v3.0
#
# This module can be used for updating grid configuration
# values in iRODS.
#
# Example:
#
# irods_gridconfig:
#  namespace: authentication
#  option_name: password_min_time
#  value: 1209600


ANSIBLE_METADATA = {
  'supported_by': 'community',
  'status': ['preview']
}

import subprocess

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec=dict(
            namespace=dict(default=None, required=True),
            option_name=dict(default=None, required=True),
            value=dict(default=None, required=True),
            ),
        supports_check_mode=True)

    namespace = module.params["namespace"]
    option_name = module.params["option_name"]
    value = module.params["value"]

    result = subprocess.run(
        ['iadmin', 'get_grid_configuration', namespace, option_name],
        capture_output = True,
        text = True,
        check = True
    )

    if (result.stderr == '' and result.stdout != ''):
        current_value = result.stdout.strip()
    else:
        module.fail_json(msg=result.stderr.strip()) # error handling can be improved once irods issue #8671 is solved

    changed = False

    if current_value != value:
        result = subprocess.run(
            ['iadmin', 'set_grid_configuration', namespace, option_name, value],
            capture_output = True,
            text = True,
            check = True
        )
        changed = True

        if (result.stderr != ''):
            module.fail_json(msg=result.stderr.strip()) # error handling can be improved once irods issue #8671 is solved

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
