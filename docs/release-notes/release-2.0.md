---
# Release Notes - Yoda v2.0

Version: 2.0

Released: TBA

## What's new
### Changes affecting functionality used by data stewards and researchers
- Add support for jumping to the file in file browsers when searching
- Add new keyword selector to metadata forms with support for controlled vocabularies
- Add SURF portal theme
- Experimental portal view and API caching
- Deprecated intake module

### Changes affecting technical administrators
- Add [support](../administration/supported-distributions.md) for Ubuntu 24.04 and AlmaLinux 9
- Add new admin privilege group (priv-admin)
- Add support for modifying resources through Ansible
- Add support for configuring NFS shares as resources

### Other changes
- iRODS: update to v4.3.4
- Python: update rulesets to 3.12
- Python-irodsclient: update to v3.1.1
- Flask and dependencies: update to v3.1.0
- Mailpit: update to v1.23.2
- GoCommands: update to v0.10.19

### Known issues
- Collections with single apex "'" in the name do not work [irods/irods#5727](https://github.com/irods/irods/issues/5727)
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python [irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54)
- Deallocation of KeyValPair results in bad AVU or error [irods/irods#8265](https://github.com/irods/irods/issues/8265)

## Upgrading from previous release
The playbook requires Ansible 2.16.x or higher.

Version constraints:
* Requires Yoda external user service to be on version 1.9.x or higher.
* Requires Yoda public server to be on version 1.9.x or higher.

1. Backup/copy custom configurations made to Yoda version 1.9.5 / 1.10.0
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Check out tag `development` of the Yoda Git repository.
```bash
git checkout development
```

4. Set the Yoda version to `development` in the configuration.
```yaml
yoda_version: development
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
