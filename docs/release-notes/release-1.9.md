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
- Support for DOI versions
- Support for multiple replication resources
- Support for configuring iRODS S3 resources
- Upgrade python-irodsclient to v1.1.5

### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)

## Upgrading from previous release
Upgrade is supported by Ansible (2.11.x).
Requires Yoda external user service to be on version 1.8.x or higher.
Requires Yoda public server to be on version 1.8.x or higher.

1. Backup/copy custom configurations made to Yoda version 1.8.
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Checkout branch `release-1.9` of the Yoda Git repository.
```bash
git checkout release-1.9
```

4. Set the Yoda version to `release-1.9` in the configuration.
```yaml
yoda_version: release-1.9
```

5. Install all Ansible collections needed to deploy Yoda:
```bash
ansible-galaxy collection install -r requirements.yml
```

6. Run the Ansible playbook in check mode.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml --check
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml --check
```

7. If the playbook has finished successfully in check mode, run the Ansible playbook normally.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml
```

8. Update all metadata JSON in the vault to latest metadata JSON version (`default-1` to `default-2`).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/check-metadata-for-schema-updates.r
```

9. Update publication endpoints if there are published packages (DataCite, landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/update-publications.r
```
