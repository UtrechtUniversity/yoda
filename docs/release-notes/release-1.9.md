---
parent: Release Notes
title: v1.9
nav_order: 89
---
# Release Notes - Yoda v1.9

Version: 1.9

Released: TBA

## What's new
### Features
- Support for vault data package versioning
- Support for configuring metadata schemas per research group
- Support for configuring retention period per research group
- Support for basic controlled vocabularies in metadata schemas
- Support for [Data Access Passwords](../design/overview/authentication.md) expiration notifications
- Support for research group retention period notifications
- Support for color mode user setting
- Support for multiple replication resources
- Support for configuring iRODS S3 resources
- Support for database connection pooling with PgBouncer
- Experimental support for [vault archiving](../design/overview/vault-archive.md) workflow
- Experimental support for groups connected to SRAM
- Upgrade iRODS to v4.2.12
- Upgrade python-irodsclient to v1.1.8
- Upgrade davrods to v1.5.1
- Upgrade to PostgreSQL 15

### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)

## Upgrading from previous release
The playbook requires Ansible 2.11.x or higher.

Version constraints:
* Requires Yoda external user service to be on version 1.9.x or higher.
* Requires Yoda public server to be on version 1.9.x or higher.

1. Backup/copy custom configurations made to Yoda version 1.8.
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Checkout branch `development` of the Yoda Git repository.
```bash
git checkout development
```

4. Set the Yoda version to `release-1.9` in the configuration.
```yaml
yoda_version: v1.9.0-beta.1
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

7. Set `postgresql_perform_db_upgrade` to `true` in the configuration to perform the database upgrase from Postgresql 9 to 15.
Optionally set `postgresql_remove_old_data_after_upgrade` to `true` in the configuration to clean up PostgreSQL 9 data and shim after the upgrade.
```yaml
postgresql_perform_db_upgrade: true
postgresql_remove_old_data_after_upgrade: false
```

8. Install all Ansible collections needed to deploy Yoda:
```bash
ansible-galaxy collection install -r requirements.yml
```

9. Run the Ansible playbook in check mode.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml --check
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml --check
```

10. If the playbook has finished successfully in check mode, run the Ansible playbook normally.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml
```

11. Update all publication metadata to support DOI versioning.
```bash
irule -r irods_rule_engine_plugin-python-instance -F /etc/irods/yoda-ruleset/tools/transform-existing-publications.r
```

12. Update all metadata JSON in the vault to latest metadata JSON version (`default-2` to `default-3`).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/check-metadata-for-schema-updates.r
```

13. Update publication endpoints if there are published packages (DataCite, landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/update-publications.r
```
