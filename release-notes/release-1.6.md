# Release notes Yoda version 1.6 (May 2020)

Version: 1.6

Released: May 2020

## What's new in Yoda version 1.6
### Features
- Improved folder browsing and sorting browse list
- Create folders from web portal
- Rename and remove files and folders from web portal
- Increase upload limit (300MB)
- Metadata format changed from XML to JSON
- Add support for geo location in metadata schemas
- Upgrade to iRODS v4.2.8.0
- Deprecate support for TLS 1.0 and TLS 1.1 (use `legacy_tls` flag to enable support for TLS 1.0 and TLS 1.1)

## Upgrading from Yoda version 1.5
Upgrade is supported by Ansible (2.9.x).
Requires Yoda external user service to be on version 1.5.x or higher.
Requires Yoda public server to be on version 1.6.x or higher.

1. Set Yoda release to `release-1.6` in configuration.
'''yaml
yoda_version: release-1.6
'''

2. Set the default schema to `default-1` in configuration.
'''yaml
default_yoda_schema: default-0
'''

3. The research ruleset (`irods-ruleset-research`) is merged with the UU ruleset (`irods-ruleset-uu`) and should be removed from the configuration (rulesets).

4. Instead of all the modules, only the extra modules are defined in the configuration. So `modules` becomes `extra_modules`:
```yaml
# Yoda modules
extra_modules:
  - name: intake
    repo: "https://github.com/UtrechtUniversity/yoda-portal-intake.git"
    dest: /var/www/yoda/yoda-portal/modules/intake
    version: "{{ yoda_version }}"
```

5. Instead of all the rulesets, only the extra rulesets are defined in the configuration. So `rulesets` becomes `extra_rulesets`:
```
# iRODS rulesets
extra_rulesets:
  - name: irods-ruleset-youth-cohort
    repo: https://github.com/UtrechtUniversity/irods-ruleset-youth-cohort.git
    ruleset_name: rules-yc
    version: "{{ yoda_version }}"
    install_scripts: no
```

6. Run the Ansible upgrade in check mode.

7. Run the Ansible upgrade.

8. Convert all metadata XML in the vault to JSON.
```bash
irule -F /etc/irods/irods-ruleset-uu/tools/check-vault-metadata-xml-for-transformation-to-json.r
```
