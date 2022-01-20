---
parent: Administration Tasks
title: Upgrading metadata schemas
nav_order: 8
---
# Upgrading metadata schemas

Metadata schemas of an Yoda instance can be migrated to newer version or other metadata schema if a transformation exists.
Only metadata in the vault space is upgraded using the steps below.
For all metadata in the research space the systems requests the user to transform the metadata to the new metadata schema.

1. Upgrade default metadata schema using Ansible or [manually](../administration/installing-metadata-schemas.md)

2. After the upgrade all metadata on the system needs to be migrated, this can be done by running the following command:
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-schema-updates.r
```
All metadata touched will be logged in the rodsLog.
Adding the schema identifiers can take some time, the batch script adds 256 jobs per 60 seconds to the rule queue.
