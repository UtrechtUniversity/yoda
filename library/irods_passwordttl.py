#!/usr/bin/python
# Copyright (c) 2021-2024 Utrecht University
# GNU General Public License v3.0

ANSIBLE_METADATA = {
  'supported_by': 'community',
  'status': ['preview']
}

import subprocess

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config_min_time=dict(default=None, required=True)
            ),
        supports_check_mode=True)

    config_min_time = int(module.params["config_min_time"])

    result = subprocess.run(
        ['iadmin', 'get_grid_configuration', 'authentication', 'password_min_time'],
        capture_output = True
    )
    current_min_time = int(result.stdout)

    changed = False

    # compare password_min_time with desired
    if current_min_time != config_min_time:
        result = subprocess.run(
            ['iadmin', 'set_grid_configuration', 'authentication', 'password_min_time', str(config_min_time)],
        )
        changed = True

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
