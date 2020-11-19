#!/usr/bin/python
# Copyright (c) 2017-2018 Utrecht University
# GNU General Public License v3.0

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

from ansible.module_utils.basic import *


IRODSCLIENT_AVAILABLE = False
try:
    import textwrap
    from irods.session import iRODSSession
    from irods.rule import Rule
except ImportError:
    pass
else:
    IRODSCLIENT_AVAILABLE = True


def get_session():
    env_file = os.path.expanduser('~/.irods/python_client_environment.json')
    with open(env_file) as data_file:
        ienv = json.load(data_file)
    return (iRODSSession(irods_env_file=env_file), ienv)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            groupName=dict(default=None, required=True),
            category=dict(default=None, required=True),
            subcategory=dict(default=None, required=True),
            description=dict(default=None, required=True),
            dataClassification=dict(default=None, required=True),
            state=dict(default="present")
        ),
        supports_check_mode=True)

    groupName = module.params["groupName"]
    category = module.params["category"]
    subcategory = module.params["subcategory"]
    description = module.params["description"]
    dataClassification = module.params["dataClassification"]
    state = module.params["state"]

    if IRODSCLIENT_AVAILABLE:
        try:
            session, ienv = get_session()
        except iRODSException:
            module.fail_json(
                msg="Could not establish irods connection. Please check ~/.irods/irods_environment.json"
            )
    else:
        module.fail_json(msg="python-irodsclient needs to be installed")

    changed = False

    # Rule to add a group to Yoda.
    rule_body = textwrap.dedent('''\
        test {{
            uuGroupAdd(*groupName, *category, *subcategory, *description, *dataClassification, *status, *message);
        }}''')

    # Rule parameters.
    input_params = {
        '*groupName': '"{groupName}"'.format(**locals()),
        '*category': '"{category}"'.format(**locals()),
        '*subcategory': '"{subcategory}"'.format(**locals()),
        '*description': '"{description}"'.format(**locals()),
        '*dataClassification': '"{dataClassification}"'.format(**locals())
    }
    output = 'ruleExecOut'

    # Execute rule.
    if not module.check_mode:
        myrule = Rule(session, body=rule_body,
                      params=input_params, output=output)
        myrule.execute()

    changed = True

    module.exit_json(
            changed=changed,
            irods_environment=ienv)


if __name__ == '__main__':
    main()
