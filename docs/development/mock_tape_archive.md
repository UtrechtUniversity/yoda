---
parent: Development
title: Mock tape archive
nav_order: 3
---
# Mock tape archive
This page describes how to use the mock DMF tape storage.
The mock DMF tape storage is installed in Yoda development environments.

## Usage:
Mock DMF tape storage is installed in a virtualenv, active to use it:
```bash
$ sudo su irods
$ cd ~
$ . dms-archive-mock/tape_archive_venv/bin/activate
```

Example to add a data object to the tape archive and put it offline:
```bash
$ iput -R mockTapeArchive test.json
$ dmattr /var/lib/irods/Vault3/home/rods/test.json
$ dmput -r /var/lib/irods/Vault3/home/rods/test.json
```

## More information
Several of the DMF commands are described here: https://www.nas.nasa.gov/hecc/support/kb/data-migration-facility-(dmf)-commands_250.html
