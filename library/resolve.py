#!/usr/bin/python
# Copyright (c) 2019 Utrecht University
# GNU General Public License v3.0

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

from ansible.module_utils.basic import *
import socket


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(default=None, required=True),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    host = module.params["host"]
    state = module.params["state"]

    module.exit_json(
            changed=False,
            ip=socket.gethostbyname(host),
            status=state)


if __name__ == '__main__':
    main()
