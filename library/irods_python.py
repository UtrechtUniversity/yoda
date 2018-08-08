#!/usr/bin/python
# Copyright (c) 2017-2018 Utrecht University
# GNU General Public License v3.0

ANSIBLE_METADATA = {
    'supported_by': 'community',
    'status': ['preview']
}

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config_path=dict(default=None, required=True),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    config_path = module.params["config_path"]
    state = module.params["state"]
    changed = False

    # Retrieve iRODS server config.
    with open(config_path, 'r+') as data_file:
        server_config = json.load(data_file)

        # Find python plugin in server config.
        found = False
        plugins = server_config["plugin_configuration"]["rule_engines"]
        for plugin in plugins:
            if plugin["plugin_name"] == "irods_rule_engine_plugin-python":
                found = True

        if not found:
            plugins.insert(1, {
                "instance_name": "irods_rule_engine_plugin-python-instance",
                "plugin_name": "irods_rule_engine_plugin-python",
                "plugin_specific_configuration": {}
            })
            changed = True

            if not module.check_mode:
                data_file.seek(0)
                json.dump(server_config, data_file, indent=4, sort_keys=True)
                data_file.truncate()

    module.exit_json(
            changed=changed,
            config_path=config_path,
            status=state)


if __name__ == '__main__':
    main()
