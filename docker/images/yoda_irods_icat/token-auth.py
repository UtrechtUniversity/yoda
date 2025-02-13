#!/usr/bin/env python3
# If you change this, change token-auth.py.j2 in the ansible as well!

import os
from datetime import datetime
from traceback import print_exc
from re import match

import sys
sys.path.append("/var/lib/irods/sqlcipher3-venv/lib64/python3.12/site-packages/")
from sqlcipher3 import dbapi2 as sqlite3

TOKEN_DB = '/etc/irods/yoda-ruleset/accesstokens.db'


def pam_sm_authenticate(pamh, flags, argv):
    try:
        user_id = pamh.get_user()
    except Exception:
        return pamh.PAM_USER_UNKNOWN

    if match("^[ -~]+$", user_id) is None:
        return pamh.PAM_AUTH_ERR

    token = pamh.authtok
    if token is None:
        return pamh.PAM_AUTH_ERR

    # This ensures that the authentication script does not create 0 byte
    # token databases, which can interfere with running the Ansible playbook.
    if not os.path.isfile(TOKEN_DB):
        return pamh.PAM_AUTH_ERR

    authenticated = False
    conn = sqlite3.connect(TOKEN_DB)

    with conn:
        try:
            conn.execute("PRAGMA key='test'")

            # Check if token matches an active token from the user.
            for row in conn.execute('''SELECT token FROM tokens WHERE user=:user_id AND exp_time > :now''',
                                    {"user_id": user_id, "now": datetime.now()}):
                if token == row[0]:
                    authenticated = True
                    break
        except Exception:
            print_exc()

    conn.close()

    if authenticated:
        return pamh.PAM_SUCCESS
    else:
        return pamh.PAM_AUTH_ERR
