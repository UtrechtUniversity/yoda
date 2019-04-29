# Release notes Yoda version 1.5 (May 2019)

Version: 1.5

Released: May 2019

## What's new in Yoda version 1.5
### Features
- New metadata form based on JSON schema
- Support for metadata schema identifiers and schema migrations
- Check for unpreservable file formats in your datasets
- Configurable number of records in file browser
- Several UX improvements to the research space
- Portal performance improvements (upgrade to PHP 7.2)
- Additional monitoring items for Zabbix
- Script to check vault data integrity

### Bug Fixes
- Fixed: CSV exports start with an empty row
- Fixed: unsubmit after submit fails in some cases

## Upgrading from Yoda version 1.4
Upgrade is supported by Ansible (2.7.x).
Requires Yoda public server and external user service to be on version 1.4.x or higher.

1. Instance specific rulesets (e.g. `irods-ruleset-i-lab`) are merged with `irods-ruleset-uu` and should be removed from the configuration (rulesets).

2. Rename default metadata schema from `default` to `default-0` in the configuration (ensure `update_schemas` is enabled).

3. Run the Ansible upgrade in check mode.

4. Run the Ansible upgrade.

5. Add a schema identifier to all metadata on the system:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-schema-updates.r
```
All metadata touched will be logged in the rodsLog.
Adding the schema identifiers can take some time, the batch script adds 256 jobs per 60 seconds to the rule queue.

6. Check if all metadata on the system has a schema identifier:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-identifier.r
```

When all metadata has a schema identifier the system default or community schema can be [upgraded](../administration/upgrading-metadata-schemas.md).
