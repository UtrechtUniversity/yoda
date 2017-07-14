#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) Paul Frederiks <paul.frederiks@gmail.com>
#
# license: GPL v3
#
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

IRODSCLIENT_AVAILABLE = False
try:
    from irods.session import iRODSSession
    from irods.models import Resource
    from irods.exception import ResourceDoesNotExist
except:
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
                name=dict(default=None, required=True),
                location=dict(default=None),
                vault=dict(default=None, type="path"),
                children=dict(default=None, type="list"),
                resourcetype=dict(default=None),
                state=dict(default="present")
                ),
            supports_check_mode=True)

    name = module.params["name"]
    location = module.params["location"]
    vault = module.params["vault"]
    children = module.params["children"]
    resourcetype = module.params["resourcetype"]

    if IRODSCLIENT_AVAILABLE:
        try:
            session, ienv = get_session()
        except:
            module.fail_json(msg="Could not establish irods connection. Please check ~/.irods/irods_environment.json")
    else:
        module.fail_json(msg="python-irodsclient needs to be installed")

    try:
        resource = session.resources.get(name)
    except ResourceDoesNotExist:
        module.fail_json(msg="Resource {} does not exists".format(name))

    module.fail_json(msg="Not implemented yet")

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
