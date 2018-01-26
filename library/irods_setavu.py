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
    from irods.models import DataObject, User, Resource, Collection
    from irods.meta import iRODSMeta
    from irods.exception import UserDoesNotExist, iRODSException
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
            irods_type=dict(default=None, required=True),
            name=dict(default=None, required=True),
            attribute=dict(default=None, required=True),
            value=dict(default=None, required=True),
            unit=dict(default=None, required=False),
            state=dict(default="present")
            ),
        supports_check_mode=True)

    models = {
            "DataObject": DataObject,
            "Collection": Collection,
            "User": User,
            "Resource": Resource}

    irods_type = module.params["irods_type"]
    try:
        model = models[irods_type]
    except KeyError:
        module.fail_json(msg="{} is not a valid irods type. Must be one of {}.".format(irods_type, ", ".join(models.keys())))

    name = module.params["name"]
    avu = iRODSMeta(
        module.params["attribute"],
        module.params["value"],
        module.params["unit"])
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
         metadata = session.metadata.get(model, name)
    except KeyError:
        module.fail_json(changed=False, msg="Could not read metadata from {} {}".format(irods_type, name))

    message = "Nothing to do"
    found = False
    for entry in metadata:
        if entry.name == avu.name:
            found = True
            if avu.value != entry.value:
                message="set {}: {} => {}: {}".format(entry.name, entry.value, avu.name, avu.value)
                changed=True
                if not module.check_mode:
                    session.metadata.set(model, name, avu)

    if not found and state == 'present':
        changed=True
        message="set {}: {}".format(avu.name, avu.value)
        if not module.check_mode:
            session.metadata.set(model, name, avu)
    elif not found and state == 'absent':
        changed=True
        message="remove {}: {}".format(avu.name, avu.value)
        if not module.check_mode:
            session.metadata.remove(model, name, avu)

    module.exit_json(changed=changed, msg=message, irods_environment=ienv)


if __name__ == '__main__':
    main()
