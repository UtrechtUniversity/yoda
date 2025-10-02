#!/usr/bin/python3

"""Initializes a Davrods lock database on an Ubuntu system.

   This does not work correctly on RHEL 9 systems because Python
   has been compiled with a different DBM backend there. So we
   use this script on an Ubuntu development environment to initialize
   an empty DBM database. The playbook then uploads a copy of this
   empty database on other environments.
"""

import argparse
import dbm.ndbm
import os
import sys


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=str,
                        help='DavRODS lock directory')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    if os.path.isdir(args.directory):
        basename = os.path.join(args.directory, "lockdb_locallock")
        dbname = os.path.join(args.directory, "lockdb_locallock.db")
    else:
        sys.exit("Error: directory does not exist")

    if os.path.exists(dbname):
        print("Not doing anything, since DB already exists.")
    else:
        with dbm.ndbm.open(basename, "n") as db:
            pass
        os.rename(dbname, basename)
