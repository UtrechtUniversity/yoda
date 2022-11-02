#!/usr/bin/python
# Copyright (c) 2017-2022 Utrecht University
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
    from irods.models import Resource
    from irods.exception import ResourceDoesNotExist, iRODSException
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
            name=dict(default=None, required=True),
            zone=dict(default=None),
            host=dict(default="EMPTY_RESC_HOST"),
            vault_path=dict(default="EMPTY_RESC_PATH", type="path"),
            children=dict(default=None, type="list"),
            resource_type=dict(default=None),
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
    context = module.params["context"]
    if not context:
        context = None

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
    warnings = []

    try:
        resource = session.resources.get(name)
    except ResourceDoesNotExist:
        if state == 'present' and not module.check_mode:
            resource = session.resources.create(
                name, resource_type, host=host,
                path=vault_path, context=context)
            changed = True
        elif state == 'absent':
            module.exit_json(changed=False, msg="Resource {} is not present".format(name))
    else:
        if state == 'absent':
            module.fail_json(msg="python-irodsclient fails to remove resources in version 0.6")
        elif state == 'present':
            if host != resource.location:
                warnings.append(
                        "Resource {name} has location set to '{resource.location}' instead of '{host}'"
                        .format(**locals()))
            if vault_path != resource.vault_path:
                warnings.append(
                        "Resource {name} has vault_path set to '{resource.vault_path}' instead of '{vault_path}'"
                        .format(**locals()))
            if resource_type != resource.type:
                warnings.append("Resource {name} has resource_type set to '{resource.type}' instead of '{resource_type}'"
                        .format(**locals()))
            if context != resource.context:
                warnings.append(
                        "Resource {name} has context set to '{resource.context}' instead of '{context}'"
                        .format(**locals()))

    # Build list of resource children names.
    names = []
    for child in resource.children:
        names.append(child.name)

    for child in children:
        if resource.children is None or child not in names:
            try:
                resource.manager.add_child(name, child)
                changed = True
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
            warnings=warnings,
            irods_environment=ienv)


if __name__ == '__main__':
    main()
