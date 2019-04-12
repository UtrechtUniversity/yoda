# Release notes Yoda version 1.5 (tba)

Version: 1.5

Released: tba

## New features since Yoda version 1.4
- New metadata form based on JSON schema
- Support for metadata schema identifiers
- Check for unpreservable files in your datasets
- Several UX improvements to the research space
- Script to check vault integrity

## Upgrading from Yoda version 1.4
Upgrade is supported by Ansible (2.7.x).

1. Instance specific rulesets (e.g. `irods-ruleset-i-lab`) are merged with `irods-ruleset-uu` and should be removed from the configuration (rulesets).

2. Rename default metadata schema from `default` to `default-0` in the configuration (ensure `update_schemas` is enabled).

3. Run the Ansible upgrade in check mode.

4. Run the Ansible upgrade.

5. After the upgrade all metadata on the system needs to be migrated to add a schema identifier.
This can be one by running the following command:
```bash
irule -F /etc/irods/irods-ruleset-research/tools/check-metadata-for-schema-updates.r
```

When all metadata has a schema identifier the system default or community schema can be [upgraded](upgrading-metadata-schemas.md).
