# Release notes Yoda version 1.6 (November 2020)

Version: 1.6

Released: November 2020

## What's new in Yoda version 1.6
### Features
- Improved folder browsing and sorting browse list
- Create folders from web portal
- Rename and remove files and folders from web portal
- Increase upload limit (300MB)
- Metadata format changed from XML to JSON
- Add support for geo location in metadata schemas
- Add support for datarequest module ([installation instructions](../administration/installing-datarequest-module.html))
- New tool to check mail configuration
- Upgrade to iRODS v4.2.7
- Deprecate support for TLS 1.0 and TLS 1.1 (use `legacy_tls` flag to enable support for TLS 1.0 and TLS 1.1)

## Upgrading from Yoda version 1.5
Upgrade is supported by Ansible (2.9.x).
Requires Yoda external user service to be on version 1.5.x or higher.
Requires Yoda public server to be on version 1.6.x or higher.

1. Backup/copy custom configurations made to Yoda version 1.5.
To view what files were changed from the defaults, run `git diff`.

2. After making sure the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Checkout branch `release-1.6` of the Yoda Git repository
```bash
git checkout release-1.6
```
This will set Yoda release to `release-1.6` in configuration as well as the default schema to `default-1`.

4. The core modules (`research`, `vault`, `statistics`, `group-manager`) are enabled by default in Yoda 1.6.
   Only extra modules have to be enabled in the configuration.
   So `modules` becomes `extra_modules` and all core modules should be removed from the `extra_modules` list.
   Update the configuration according to your specifications.
   For example:
    ```yaml
        # Yoda modules
        extra_modules:
          - name: intake
            repo: "https://github.com/UtrechtUniversity/yoda-portal-intake.git"
            dest: /var/www/yoda/yoda-portal/modules/intake
            version: "\{\{ yoda_version \}\}"
    ```

5. The core rulesets (`core` and `irods-ruleset-uu`) are enabled by default in Yoda 1.6.
   Only extra modules have to be enabled in the configuration.
   Furthermore, the research ruleset (`irods-ruleset-research`) has been merged with the UU ruleset
   (`irods-ruleset-uu`). So `rulesets` becomes `extra_rulesets`;
   `core`, `irods-ruleset-research` and `irods-ruleset-uu` should be removed from the `extra_rulesets` list.
   Update the configuration according to your specifications.
   For example:
    ```yaml
        # iRODS rulesets
        extra_rulesets:
          - name: irods-ruleset-youth-cohort
            repo: https://github.com/UtrechtUniversity/irods-ruleset-youth-cohort.git
            ruleset_name: rules-yc
            version: "\{\{ yoda_version \}\}"
            install_scripts: no
    ```

6. Run the Ansible playbook in check mode.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml --check
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml --check
```

7. If the playbook has finished succesfully in check mode, run the Ansible playbook normally.
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml
```

8. Convert all metadata XML in the vault to JSON (`default-0` XML to `default-0` JSON).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/check-vault-metadata-xml-for-transformation-to-json.r
```

9. Update all metadata JSON in the vault to latest metadata JSON version (`default-0` to `default-1`).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/check-metadata-for-schema-updates.r
```

10. Update publication endpoints if there are published packages (landingpages and OAI-PMH)):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/update-publications.r
```
