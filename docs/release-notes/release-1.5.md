# Release notes Yoda version 1.5 (July 2019)

Version: 1.5

Released: July 2019

## What's new in Yoda version 1.5
### Features
- New metadata form based on JSON schema
- Research and vault space are split into separate modules
- Add support for upload and download (25MB up / unlimited download)
- Add support for viewing media in the portal
- Support for metadata schema identifiers and schema migrations
- Check for unpreservable file formats in your datasets
- Configurable number of records in file browser
- Provenance information is written to vault packages in a file
- Several UX improvements to the research space
- Portal performance improvements (upgrade to PHP 7.2)
- Upgrade CodeIgniter framework to latest release (v3.1.10)
- Additional monitoring items for Zabbix
- Script to check vault data integrity

### Bug Fixes
- Fixed: CSV exports start with an empty row
- Fixed: unsubmit after submit fails in some cases

## Upgrading from Yoda version 1.4
Upgrade is supported by Ansible (2.7.x).
Requires Yoda public server and external user service to be on version 1.4.x or higher.

1. Set Yoda release to release-1.5 in configuration.

2. Add vault module to portal modules configuration.

3. Instance specific rulesets (e.g. `irods-ruleset-i-lab`) are merged with `irods-ruleset-uu` and should be removed from the configuration (rulesets).

4. Rename default metadata schema from `default` to `default-0` in the configuration (ensure `update_schemas` is enabled).

5. Run the Ansible upgrade in check mode.

6. Run the Ansible upgrade.

7. Add a schema identifier to all metadata on the system:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-schema-updates.r
```
All metadata touched will be logged in the rodsLog.
Adding the schema identifiers can take some time, the batch script adds 256 jobs per 60 seconds to the rule queue.

8. Check if all metadata on the system has a schema identifier:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-identifier.r
```

9. Update all landingpages with the new layout:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/update-landingpages.r
```
