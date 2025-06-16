---
parent: Development
title: Mock tape archive
nav_order: 4
---
# Mock tape archive
This page describes how to use the mock DA tape storage.
The mock DA tape storage is installed in Yoda development environments.

## Usage:
Mock DA tape storage is installed in a virtualenv, active to use it:
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
Several of the DA commands are described [here](https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/166920963/DAcommands+Documentation)
