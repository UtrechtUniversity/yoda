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
    from irods.exception import ResourceDoesNotExist, iRODSException
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
            zone=dict(default=None),
            host=dict(default="EMPTY_RESC_HOST"),
            vault_path=dict(default="EMPTY_RESC_PATH", type="path"),
            children=dict(default=None, type="list"),
            resource_type=dict(default=None),
            resource_class=dict(default=None),
            context=dict(default=None),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    name = module.params["name"]
    host = module.params["host"]
    vault_path = module.params["vault_path"]
    children = module.params["children"]
    if children is None:
        children = []

    resource_type = module.params["resource_type"]
    resource_class = module.params["resource_class"]
    context = module.params["context"]
    state = module.params["state"]

    if IRODSCLIENT_AVAILABLE:
        try:
            session, ienv = get_session()
        except:
            module.fail_json(msg="Could not establish irods connection. Please check ~/.irods/irods_environment.json")
    else:
        module.fail_json(msg="python-irodsclient needs to be installed")


    changed = False


    try:
        resource = session.resources.get(name)
    except ResourceDoesNotExist:
        if state == 'present' and not module.check_mode:
            resource = session.resources.create(name, resource_type, host=host, path=vault_path, context=context, resource_class=resource_class)
            changed = True
        elif state == 'absent':
            module.exit_json(changed=False, msg="Resource {} is not present".format(name))
    else:
        if state == 'absent':
            module.fail_json(msg="python-irodsclient fails to remove resources in version 0.6")

    for child in children:
        if resource.children is None or child not in resource.children:
            try:
                resource.manager.add_child(name, child)
            except iRODSException:
                module.fail_json(msg="iRODSException while adding {} as a child to {}".format(child, name))
            changed = True


    module.exit_json(
            changed=changed,
            resource=dict(
                name=resource.name,
                zone=resource.zone_name,
                parent=resource.parent,
                context=resource.context,
                status=resource.status),
            irods_environment=ienv)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
