#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# copyright Utrecht University
#
# license: GPL v3
#
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config_path=dict(default=None, required=True),
            rulesets=dict(default=None, type="list", required=True),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    config_path = module.params["config_path"]
    rulesets = module.params["rulesets"]
    if rulesets is None:
        rulesets = []
    state = module.params["state"]
    changed = False

    # Retrieve iRODS server config.
    with open(config_path, 'r+') as data_file:
        server_config = json.load(data_file)

        # Find all rulesets in server config.
        active_rulesets = []
        for item in server_config['re_rulebase_set']:
            active_rulesets.append(item['filename'])

        # Check if all rulesets are present.
        if active_rulesets != rulesets:
            server_config['re_rulebase_set'] = []
            for ruleset in rulesets:
                server_config['re_rulebase_set'].append({'filename': ruleset})
                data_file.seek(0)
                json.dump(server_config, data_file, indent=4, sort_keys=True)
                data_file.truncate()
                changed = True

    module.exit_json(
            changed=changed,
            config_path=config_path,
            rulesets=rulesets,
            status=state)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
