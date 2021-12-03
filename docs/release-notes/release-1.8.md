---
parent: Release Notes
title: v1.8
nav_order: 90
---
# Release Notes - Yoda v1.8

Version: 1.8

Released: TBA

## What's new
### Features
- [Full theming support](../design/overview/theme-packages.md)
- Support for [Data Access Passwords](../design/overview/authentication.md)
- Support for user settings
- Support for notifications
- Support for copy and move actions in the web portal
- Support for multi-select actions for files and folders in research space
- Improved search module and new search bar in header
- Several UX improvements to default theme
- Upgrade to iRODS v4.2.10
- Removed `legacy_tls` flag (legacy TLS support, TLS 1.0 and 1.1)

### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Server leaks memory via Python rule genqueries and built-in microservices [irods/irods#4649](https://github.com/irods/irods/issues/4649)
- iQuest fails when select is used in argument string [irods/irods#4697](https://github.com/irods/irods/issues/4697)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)
- Long PAM password/token string causes PACKSTRUCT error [python-irodsclient#279](https://github.com/irods/python-irodsclient/issues/279)
- Executing a rule requires reconnection / reauthentication to iRODS [python-irodsclient#190](https://github.com/irods/python-irodsclient/issues/190)

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

4. Run the Ansible playbook in check mode.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml --check
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml --check
```

5. If the playbook has finished succesfully in check mode, run the Ansible playbook normally.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml
```

6. Update publication endpoints if there are published packages (DataCite, landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/update-publications.r
```
