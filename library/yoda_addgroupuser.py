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
    env_file = os.path.expanduser('~/.irods/irods_environment.json')
    with open(env_file) as data_file:
        ienv = json.load(data_file)
    return (iRODSSession(irods_env_file=env_file), ienv)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            groupName=dict(default=None, required=True),
            user=dict(default=None, required=True),
            role=dict(default=None, required=True),
            state=dict(default="present")
        ),
        supports_check_mode=True)

    groupName = module.params["groupName"]
    user = module.params["user"]
    role = module.params["role"]
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

    # Rule to add an user to a group in Yoda.
    rule_body = '''
                   uuGroupUserAdd(*groupName, *user, *status, *message);
                   uuGroupUserChangeRole(*groupName, *user, *role, *status, *message);
                '''
    # Rule parameters.
    input_params = {
        '*groupName': '"{groupName}"'.format(**locals()),
        '*user': '"{user}"'.format(**locals()),
        '*role': '"{role}"'.format(**locals())
    }

    # Execute rule.
    if not module.check_mode:
        myrule = Rule(session,
                      instance_name='irods_rule_engine_plugin-irods_rule_language-instance',
                      body=rule_body,
                      params=input_params,
                      output='ruleExecOut')
        myrule.execute()

    changed = True

    module.exit_json(
            changed=changed,
            irods_environment=ienv)


if __name__ == '__main__':
    main()
