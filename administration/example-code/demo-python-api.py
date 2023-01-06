#!/usr/bin/env python3

"""Example script that shows how to connect to Yoda using python-irodsclient
   (iRODS's Python API) and perform a GenQuery"""

from getpass import getpass
import json
import ssl
import sys

from irods.models import Collection
from irods.session import iRODSSession

def get_irods_environment(irods_environment_file="irods_environment.json"):
    """Reads the irods_environment.json file, which contains the environment
       configuration."""
    with open(irods_environment_file, 'r') as f:
        return json.load(f)


def setup_session(irods_environment_config, require_ssl = True, ca_file = "cacert.pem"):
    """Use irods environment files to configure a iRODSSession"""

    password = getpass(prompt="Please provide your irods password:")

    if require_ssl:
        ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=ca_file, capath=None, cadata=None)
        ssl_settings = {'client_server_negotiation': 'request_server_negotiation',
                        'client_server_policy': 'CS_NEG_REQUIRE',
                        'encryption_algorithm': 'AES-256-CBC',
                        'encryption_key_size': 32,
                        'encryption_num_hash_rounds': 16,
                        'encryption_salt_size': 8,
                        'ssl_context': ssl_context}
        session = iRODSSession(
            irods_password=password,
            **irods_environment_config,
            **ssl_settings
        )
    else:
        session = iRODSSession(
            password=password,
            **irods_environment_config,
        )

    return session

# Create a session
env_config = get_irods_environment()
session = setup_session(env_config)

if session is None:
    print("Error: unable to create session.")
    sys.exit(1)

# Now that we have a session, we can talk to iRODS using the
# python-irodsclient API. This example query shows a list of
# groups you have access to:
with session as s:
    home_collection = "/{}/home".format(s.zone)
    collections = (s.query(Collection.name)
                   .filter(Collection.parent_name == home_collection)
                   .get_results())
    for c in sorted(collections, key=lambda d: d[Collection.name]):
        print(c[Collection.name])
