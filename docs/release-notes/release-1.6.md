# Release notes Yoda version 1.6 (TBA)

Version: 1.6

Released: TBA

## What's new in Yoda version 1.6
### Features
- Research and vault space are split into separate modules
- Add support for upload and download in research space
- Add support for viewing media in the portal
- Provenance information is written to vault packages in a file
- Upgrade CodeIgniter framework to latest release (v3.1.10)

### Bug Fixes


## Upgrading from Yoda version 1.5
Upgrade is supported by Ansible (2.7.x).

1. Set Yoda release to release-1.6 in configuration.

2. Add vault module to portal modules configuration.

3. Run the Ansible upgrade in check mode.

4. Run the Ansible upgrade.

5. Check if all metadata on the system has a schema identifier:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-identifier.r
```

6. If not all metadata has a schema identifier add a schema identifier:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-schema-updates.r
```
All metadata touched will be logged in the rodsLog.
Adding the schema identifiers can take some time, the batch script adds 256 jobs per 60 seconds to the rule queue.

7. When all metadata has a schema identifier the system default or community schema can be [upgraded](../administration/upgrading-metadata-schemas.md).
