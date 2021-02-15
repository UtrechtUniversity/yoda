# Release notes Yoda version 1.7 (TBA)

Version: 1.7

Released: TBA

## What's new in Yoda version 1.7
### Features
- Theming capability for all available Yoda modules using Bootstrap 4
- API access for all currently used functionality used by the Yoda frontend for all modules
- Two specific metadata forms (HPTlab and Teclab) for Utrecht University Geo Faculty
- As a Yoda administrator it is possible to send a test email (through Yoda from the command line) so email settings can be tested
- A researcher can now add a CC-0 (Creative Commons zero) license for research data so sharing published data is conform this license
- As a researcher I want my datacite record updated when datacite mapping is changed so that my dataset is found

### Known issues
- When datapackage is secured to the vault, and directly after the metadata is edited and saved in the research area, the file metadata.json will be shown twice for a brief period of time (<5 minutes)


## Upgrading from Yoda version 1.6
Upgrade is supported by Ansible (2.9.x).
Requires Yoda external user service to be on version 1.5.x or higher.
Requires Yoda public server to be on version 1.6.x or higher.

1. Backup/copy custom configurations made to Yoda version 1.6.
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Checkout branch `release-1.7` of the Yoda Git repository.
```bash
git checkout release-1.7
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

6. Update publication endpoints if there are published packages (landingpages and OAI-PMH)):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/update-publications.r
```
