---
parent: Administration Tasks
title: Upgrading metadata schemas
nav_order: 8
---
# Upgrading metadata schemas

When a newer version of a metadata schema becomes available, it can be necessary or useful to transform
existing metadata of archived data packages to the new schema version. Yoda can usually handle such transformations
(partially) automatically for the default metadata schemas. Details are typically provided
in the release notes of the Yoda version that introduces the new schema.

In general, you need to follow these steps:

1. First, configure the groups you want to upgrade to use the new metadata schema version. In Yoda, schemas can
   be configured on various levels (see [the design documentation](../design/metadata/schema-configuration.md)
   for details. You need to ensure that the configuration at each level is correct. For example, if you want to update
   all vault groups to a new metadata schemas on an environment where some groups use a group-level setting whereas others
   use an environment-level setting, you need to update the settings at both levels.

   For upgrading the environment or category default metadata schema,
   see [the instructions for installing metadata schemas](../administration/installing-metadata-schemas.md).

   For updating group level schema settings, you can use the imeta command as a rodsadmin user. For example:

   ```bash
   imeta set -u research-foo schema_id default-3
   ```

2. If you want to check all archived data packages on the environment for schema updates, use the generic rule:

   ```bash
   irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/check-metadata-for-schema-updates.r
   ```

   All metadata transformations will be logged in the rodsLog.  Adding the schema identifiers can take some time, as the
   job will use delays between checking data packages.

   If you only want to check individual archived data packages for schema updates, use the rule
   for checking individual data packages. For example:

   ```bash
   irule -r irods_rule_engine_plugin-python-instance -F tools/check-single-dp-metadata-for-schema-updates.r '*collection="/tempZone/home/vault-foo/datapackage[123456789]"'
   ```
