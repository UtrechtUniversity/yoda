# Release notes Yoda version 1.6 (TBA)

Version: 1.6

Released: TBA

## What's new in Yoda version 1.6
### Features
- Metadata format changed from XML to JSON
- Add support for geo location in metadata schemas
-
## Upgrading from Yoda version 1.5
Upgrade is supported by Ansible (2.8.x).
Requires Yoda external user service to be on version 1.5.x or higher.
Requires Yoda public server to be on version 1.6.x or higher.

1. Set Yoda release to release-1.6 in configuration.
'''yaml
yoda_version: release-1.6
'''

2. Run the Ansible upgrade in check mode.

3. Run the Ansible upgrade.

4. Convert all metadata XML in the vault to JSON
```bash
irule -F /etc/irods/irods-ruleset-uu/tools/check-vault-metadata-xml-for-transformation-to-json.r
```
