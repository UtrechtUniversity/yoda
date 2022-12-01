#!/usr/bin/python
# Copyright (c) 2018-2022 Utrecht University
# GNU General Public License v3.0

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(default=None, required=True),
            key=dict(default=None, required=True),
            value=dict(default=None, required=True),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    path = module.params["path"]
    key = module.params["key"]
    if key == "db_port":
        value = int(module.params["value"])
    else:
        value = module.params["value"]
    state = module.params["state"]
    changed = True

    # Retrieve postgres configuration.
    with open(path, 'r+') as data_file:
        irods_config = json.load(data_file)
        postgres = irods_config["plugin_configuration"]["database"]["postgres"]

        # Check if postgres config variable already exists.
        if key in postgres:
            # Check if postgres config variable has correct value.
            if postgres[key] == value:
                changed = False
            else:
                # Set postgres config variable.
                postgres[key] = value
        else:
            # Set postgres config variable.
            postgres[key] = value

        if not module.check_mode:
            data_file.seek(0)
            json.dump(irods_config, data_file, indent=4, sort_keys=True)
            data_file.truncate()

    module.exit_json(
            changed=changed,
            path=path,
            key=key,
            value=value,
            status=state)


if __name__ == '__main__':
    main()
