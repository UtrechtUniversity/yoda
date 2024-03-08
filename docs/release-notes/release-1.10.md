---
# Release Notes - Yoda v1.10

Version: 1.10

Released: TBA

## What's new
### Features
- Support for Ubuntu 20.04 LTS

### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)

## Upgrading from previous release
Upgrade is supported by Ansible (2.11.x).
Requires Yoda external user service to be on version 1.9.x or higher.
Requires Yoda public server to be on version 1.9.x or higher.

(TODO: add upgrade procedure)
