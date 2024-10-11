---
# Release Notes - Yoda v1.10

Version: 1.10

Released: 11 October 2024

## What's new
### Features
- Support for Ubuntu 20.04 LTS
- Support for multiple deposit groups
- Support for landingpage themes
- Added new Administration page, enables functional administration task in the portal
- Added new Data Transfer page, with ready to use configurations for data transfers
- Removed RADIUS fallback option
- Removed `Secured` status from research space
- Improved copy to vault with irsync
- Improved support for [vault archiving](../design/overview/vault-archive.md) workflow
- Improved performance in portal
- Upgrade python-irodsclient to v2.1.0

### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)

## Upgrading from previous release
The playbook requires Ansible 2.11.x or higher. Ansible 2.17.0 and higher is not yet supported.

Version constraints:
* Requires Yoda external user service to be on version 1.9.x or higher.
* Requires Yoda public server to be on version 1.9.x or higher.

Configuration changes:
* Yoda 1.10 blocks remote access to the anonymous account via the iRODS protocol by default. If you run DavRODS on a different server from the provider, you need to add
  its network address to the `irods_anonymous_account_permit_addresses` configuration parameter.

1. Backup/copy custom configurations made to Yoda version 1.9.
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Check out tag `v1.10.0` of the Yoda Git repository.
```bash
git checkout v1.10.0
```

4. Set the Yoda version to `v1.10.0` in the configuration.
```yaml
yoda_version: v1.10.0
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

8. Update publication endpoints if there are published packages (DataCite, landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/update-publications.r
```
