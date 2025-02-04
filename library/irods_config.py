#!/usr/bin/python
# Copyright (c) 2017-2018 Utrecht University
# GNU General Public License v3.0
#
# This module facilitates updating settings in a JSON configuration file
# (such as the iRODS server_config.json file)
#
# Example for updating a top-level key:
#  path: /etc/irods/server_config.json
#  key: icat_host
#  value: combined.yoda.test
#
# When updating a nested key, use the key_separator argument to make
# the key specify the path to the nested key. For example:
#
#  path: /etc/irods/server_config.json
#  key: log_level/agent
#  key_separator: /
#  value: info

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
            key_separator=dict(default=None),
            convert_int=dict(default="no"),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    path = module.params["path"]
    key = module.params["key"]
    key_separator = module.params["key_separator"]
    state = module.params["state"]
    convert_int = module.params["convert_int"]
    value = int(module.params["value"]) if convert_int != "no" else module.params["value"]

    changed = False

    # Retrieve iRODS environment.
    with open(path, 'r+') as data_file:
        irods_config = json.load(data_file)
        *outer_keys, inner_key = [key] if key_separator is None else key.split(key_separator)

        current_dict = irods_config
        for key in outer_keys:
            lookup_value = current_dict.get(key, None)
            if lookup_value is not None and isinstance(lookup_value, dict):
                current_dict = lookup_value
            else:
                new_dict = dict()
                current_dict[key] = new_dict
                current_dict = new_dict
                changed = True

        # Check if iRODS config variable already exists.
        if inner_key in current_dict:
            # Check if iRODS config variable has correct value.
            if current_dict[inner_key] != value:
                current_dict[inner_key] = value
                changed = True
        else:
            # Set iRODS config variable.
            changed = True
            current_dict[inner_key] = value

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
