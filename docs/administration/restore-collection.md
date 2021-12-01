---
parent: Administration Tasks
title: Restore collection
nav_order: 13
---
# Restore collection
If you want to restore a collection you can use the `restore-collection.r` tool from the `irods-ruleset-uu`.
The tool is located at `/etc/irods/irods-ruleset-uu/tools/restore-collection.r`

The tool accepts the following parameters:

Parameter   | Description
------------|---------------------------------------------
path	      | Path to collection to restore
timestamp   | UNIX timestamp, restore collection to revision from before this timestamp
restorePath | Path to restore the collection to, empty if you want to restore in the same collection

## Examples:
```bash
irule -F restore-collection.r "*path='/tempZone/home/research-test'" "*timestamp=1540819891"
```
Restore the collection `/tempZone/home/research-test` with revision before `1540819891` (Mon Oct 29 14:31:31 2018 CET).

```bash
irule -F restore-collection.r "*path='/tempZone/home/research-test'" "*timestamp=1540819891" "*restorePath='/tempZone/home/research-test/restore'"
```
Restore the collection `/tempZone/home/research-test` with revision before `1540819891` (Mon Oct 29 14:31:31 2018 CET) into collection `/tempZone/home/research-test/restore`.
