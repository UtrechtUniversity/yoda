---
parent: Development
title: Data Archive Mock
nav_order: 4
---
# Data Archive Mock
This page describes how to use the Data Archive mock (tape storage).
The Data Archive mock is installed in Yoda development environments.

## Usage:
The Data Archive mock is installed in a virtualenv; activate it to use it:
```bash
$ sudo su irods
$ cd ~
$ . data-archive-mock/data_archive_venv/bin/activate
```

Example to add a data object to the tape archive and put it offline:
```bash
$ iput -R mockDataArchive test.json
$ daattr /var/lib/irods/Vault3/home/rods/test.json
$ darelease /var/lib/irods/Vault3/home/rods/test.json
```

## More information
Several of the Data Archive commands are described here: https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/166920963/DAcommands+Documentation
