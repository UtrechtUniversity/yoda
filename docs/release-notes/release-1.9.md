---
parent: Release Notes
title: v1.9
nav_order: 89
---
# Release Notes v1.9

Version: 1.9

Released: February 2024

## What's new
### Features
- Support for vault data package versioning
- Support for configuring metadata schemas per research group
- Support for configuring retention period per research group
- Support for basic controlled vocabularies in metadata schemas
- Support for Creative Commons (BY-ND, BY-NC, BY-NC-ND) and GPL v3 licenses
- Support for [Data Access Passwords](../design/overview/authentication.md) expiration notifications
- Support for research group retention period notifications
- Support for CSV group imports
- Support for color mode user setting
- Support for multiple replication resources
- Support for configuring iRODS S3 resources
- Support for database connection pooling with PgBouncer
- Support for [Automatic Resource Balancing](../design/processes/automatic-resource-balancing.md)
- Support for viewing text files in portal
- Support for multiple deposit groups
- Support for groups connected to SRAM
- Experimental support for [vault archiving](../design/overview/vault-archive.md) workflow
- Improved overwrite actions in research space
- Upgrade iRODS to v4.2.12
- Upgrade python-irodsclient to v1.1.9
- Upgrade davrods to v1.5.1
- Upgrade to PostgreSQL 15

### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)

## Upgrading from previous release
The playbook requires Ansible 2.11.x or higher. Ansible 2.17.0 and higher is not yet supported.

Version constraints:
* Requires Yoda external user service to be on version 1.9.x or higher.
* Requires Yoda public server to be on version 1.9.x or higher.

1. Backup/copy custom configurations made to Yoda version 1.8.
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Checkout tag `v1.9.3` of the Yoda Git repository.
```bash
git checkout v1.9.3
```

4. Set the Yoda version to `v1.9.3` in the configuration.
```yaml
yoda_version: v1.9.3
```

5. Change the default schema from `default-2` to `default-3` in the configuration.
Person identifiers must be valid and new dependency between license and data access restriction.
This requires an intervention by the responsible datamanager beforehand.
```yaml
default_yoda_schema: default-3
```

6. Metadata schemas are configurable per research group.
To configure the metadata schemas available the `metadata_schemas` configuration can be used.
See also [this](../administration/installing-metadata-schemas.md) documentation for more information on installing metadata schemas.
```yaml
metadata_schemas:
  - name: default-2
    install: true
    active: false
  - name: default-3
    install: true
    active: true
```

7. Yoda version 1.9 restricts access to the anonymous account. If you run DavRODS on a separate server from the provider, you need to configure Yoda to permit access to the anonymous account from the DavRODS server using the new irods_anonymous_account_permit_addresses [configuration](../administration/configuring-yoda.md) parameter.

8. If you use the External User Service (EUS): some EUS parameters have changed from Yoda 1.8 to 1.9. Yoda 1.9 performs server certificate validation of requests from the provider to the EUS server by default. This can be disabled by setting `eus_api_tls_verify` to `false`. For some SMTP parameters, EUS uses joint parameters with the provider in Yoda 1.9. Please see the [configuration guide](../administration/configuring-yoda.md) for more information.
```
| Old parameter (1.8) | New parameter  | Notes                                |
|---------------------|----------------|--------------------------------------|
| eus_smtp_host       | smtp_server    | New format. e.g. smtp://localhost:25 |
| eus_smtp_port       | smtp_server    | New format. e.g. smtp://localhost:25 |
| eus_smtp_auth       | smtp_auth      |                                      |
| eus_smtp_security   | smtp_server    | New format. e.g. smtp://localhost:25 |
```

9. Unless your Yoda environment has already been upgraded to PostgreSQL 15, you should upgrade PostgreSQL during or immediately after the Yoda upgrade. Please consult [the PostgreSQL upgrade information page](../administration/upgrading-postgresql.md) for information about how to perform the upgrade. Example configuration:
```yaml
postgresql_perform_db_upgrade: true
postgresql_remove_old_data_after_upgrade: false
```

10. Install all Ansible collections needed to deploy Yoda:
```bash
ansible-galaxy collection install -r requirements.yml
```

11. Run the Ansible playbook in check mode.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml --check
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml --check
```

12. If the playbook has finished successfully in check mode, run the Ansible playbook normally.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml
```

13. Update statistics storage data to the latest format.
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/transform-storage-data.r
```

14. Report vault data package metadata containing invalid ORCID person identifiers.
```bash
irule -r irods_rule_engine_plugin-python-instance -F /etc/irods/yoda-ruleset/tools/metadata/vault-check-orcid-format.r
```

15. Correct vault data package metadata containing invalid ORCID person identifiers.
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/metadata/vault-correct-orcid-format.r
```

16. Update all publication metadata to support DOI versioning.
```bash
irule -r irods_rule_engine_plugin-python-instance -F /etc/irods/yoda-ruleset/tools/transform-existing-publications.r
```

17. Update all metadata JSON in the vault to latest metadata JSON version (`default-2` to `default-3`).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/check-metadata-for-schema-updates.r
```

18. Update publication endpoints if there are published packages (DataCite, landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/update-publications.r
```
