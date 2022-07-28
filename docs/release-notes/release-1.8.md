---
parent: Release Notes
title: v1.8
nav_order: 90
---
# Release Notes - Yoda v1.8

Version: 1.8

Released: July 2022

## What's new
### Features
- [Full theming support](../design/overview/theme-packages.md)
- Support for [Data Access Passwords](../design/overview/authentication.md)
- Support for user settings
- Support for notifications
- Support for copy and move actions in the web portal
- Support for multi-select actions for files and folders in research space
- Support for davrods server on separate host
- Support for [Data Package References](../design/overview/data_package_reference.md)
- Improvements to default schema (`default-2`)
- Transformation from `default-1` to `teclab-0` / `hptlab-0`
- Improved search module and new search bar in header
- DataCite connection uses REST API instead of legacy MDS
- Several UX improvements to default theme
- Upgrade iRODS to v4.2.11
- Upgrade python-irodsclient to v1.1.3
- Removed `legacy_tls` flag (legacy TLS support, TLS 1.0 and 1.1)


### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)

## Upgrading from previous release
Upgrade is supported by Ansible (2.9.x).
Requires Yoda external user service to be on version 1.5.x or higher.
Requires Yoda public server to be on version 1.6.x or higher.

1. Backup/copy custom configurations made to Yoda version 1.7.
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Checkout branch `release-1.8` of the Yoda Git repository.
```bash
git checkout release-1.8
```

4. Change the default schema from `default-1` to `default-2` in configuration.
Discipline must be present in all vault packages before migration.
I.e. discipline must be manually added if not present yet.
This requires an intervention by the responsible datamanager beforehand.
```yaml
default_yoda_schema: default-2
```

5. Two OpenID Connect configuration options are added and one has been replaced. If OIDC is active (`oidc_active`), make sure you have [configured](../administration/configuring-openidc.md), `oidc_jwks_uri` and `oidc_jwt_issuer`. Option `oidc_domain` is replaced with `oidc_domains`. Example:
```yaml
oidc_domains: ['domain1.tld', 'domain2.tld']
```

6. DataCite connection is now using REST API instead of legacy MDS. If DataCite is configured the option `datacite_server` should be replaced with `datacite_rest_api_url`. Example:
```yaml
datacite_rest_api_url: api.test.datacite.org
```

7. Install all Ansible collections needed to deploy Yoda:
```bash
ansible-galaxy collection install -r requirements.yml
```

8. Run the Ansible playbook in check mode.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml --check
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml --check
```

9. If the playbook has finished successfully in check mode, run the Ansible playbook normally.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml
```

10. Update all metadata JSON in the vault to latest metadata JSON version (`default-1` to `default-2`).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/check-metadata-for-schema-updates.r
```

11. Update publication endpoints if there are published packages (DataCite, landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/update-publications.r
```
