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
    from irods.session import iRODSSession
    from irods.models import User
    from irods.exception import UserDoesNotExist, iRODSException
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
            name=dict(default=None, required=True),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    name = module.params["name"]
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

    try:
        resource = session.users.get(name)
    except UserDoesNotExist:
        if state == 'present' and not module.check_mode:
            resource = session.users.create(name, "rodsuser")
            changed = True
        elif state == 'absent':
            module.exit_json(changed=False, msg="User {} is not present".format(name))

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
