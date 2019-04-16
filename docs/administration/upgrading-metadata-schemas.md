# Upgrading metadata schemas

Metadata schemas of an Yoda instance can be migrated to newer version or other metadata schema if a transformation exists.

1. Upgrade default metadata schema using Ansible or [manually](../administration/installing-metadata-schemas.html)

2. After the upgrade all metadata on the system needs to be migrated, this can be one by running the following command:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-schema-updates.r
```
