---
parent: Administration Tasks
title: Deprovision users
nav_order: 16
---
# Deprovision Users
Instructions for deprovisioning users.

All the users of the Yoda instance that are not a member of any existing groups can be deprovisioned in the following steps:

Generate a list of users to be deprovisioned by using the following command:
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/deprovision-users.r
```
The iRODS admin can then delete the enlisted users by using the following command:
```bash
iadmin rmuser ${USERNAME}
```
