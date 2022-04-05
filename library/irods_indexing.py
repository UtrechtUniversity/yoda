#!/usr/bin/python
# Copyright (c) 2021 Utrecht University
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
      index_server=dict(default=None, required=True),
      state=dict(default="present")
      ),
    supports_check_mode=True)

  config_path = module.params["config_path"]
  index_server = module.params["index_server"]
  state = module.params["state"]
  changed = False

  # Retrieve iRODS server config.
  with open(config_path, 'r+') as data_file:
    server_config = json.load(data_file)

    # Find indexing plugin in server config.
    found = False
    plugins = server_config["plugin_configuration"]["rule_engines"]
    for plugin in plugins:
      if plugin["plugin_name"] == "irods_rule_engine_plugin-indexing":
        found = True
      if plugin["plugin_name"] == "irods_rule_engine_plugin-cpp_default_policy":
        default_policy = plugin

    if not found:
      plugins.remove(default_policy)
      plugins.extend([
        {
          "instance_name": "irods_rule_engine_plugin-indexing-instance",
          "plugin_name": "irods_rule_engine_plugin-indexing",
          "plugin_specific_configuration": {}
        },
        {
          "instance_name": "irods_rule_engine_plugin-elasticsearch-instance",
          "plugin_name": "irods_rule_engine_plugin-elasticsearch",
          "plugin_specific_configuration": {
            "hosts": ["http://" + index_server + ":9200/"],
            "es_version": "7.x",
            "bulk_count": 100,
            "read_size": 4194304
          }
        },
        {
          "instance_name": "irods_rule_engine_plugin-document_type-instance",
          "plugin_name": "irods_rule_engine_plugin-document_type",
          "plugin_specific_configuration": {}
        },
        default_policy
      ])
      changed = True
    elif plugins[-1] != default_policy:
      plugins.remove(default_policy)
      plugins.append(default_policy)
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
