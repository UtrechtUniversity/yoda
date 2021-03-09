# Release notes Yoda version 1.8 (TBA)

Version: 1.8

Released: TBA

## What's new in Yoda version 1.8
### Features
- Support for UI templates
- Support for notifications

## Upgrading from Yoda version 1.7
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
