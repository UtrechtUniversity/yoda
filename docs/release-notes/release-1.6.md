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

1. Set Yoda release to `release-1.6` in configuration.
```yaml
yoda_version: release-1.6
```

2. Set the default schema to `default-1` in configuration.
```yaml
default_yoda_schema: default-1
```

3. The core modules (`research`, `vault`, `statistics`, `group-manager`) are enabled by default in Yoda 1.6.
   Only extra modules have to be enabled in the configuration.
   So `modules` becomes `extra_modules` and all core modules should be removed from the `extra_modules` list.
   For example:
    ```yaml
        # Yoda modules
        extra_modules:
          - name: intake
            repo: "https://github.com/UtrechtUniversity/yoda-portal-intake.git"
            dest: /var/www/yoda/yoda-portal/modules/intake
            version: "{{ yoda_version }}"
    ```

4. The core rulesets (`core` and `irods-ruleset-uu`) are enabled by default in Yoda 1.6.
   Only extra modules have to be enabled in the configuration.
   Furthermore, the research ruleset (`irods-ruleset-research`) has been merged with the UU ruleset
   (`irods-ruleset-uu`). So `rulesets` becomes `extra_rulesets`;
   `core`, `irods-ruleset-research` and `irods-ruleset-uu` should be removed from the `extra_rulesets` list.
   For example:
    ```yaml
        # iRODS rulesets
        extra_rulesets:
          - name: irods-ruleset-youth-cohort
            repo: https://github.com/UtrechtUniversity/irods-ruleset-youth-cohort.git
            ruleset_name: rules-yc
            version: "{{ yoda_version }}"
            install_scripts: no
    ```

5. Run the Ansible upgrade in check mode.

6. Run the Ansible upgrade.

7. Convert all metadata XML in the vault to JSON (`default-0` XML to `default-0` JSON).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/check-vault-metadata-xml-for-transformation-to-json.r
```

8. Update all metadata JSON in the vault to latest metadata JSON version (`default-0` to `default-1`).
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/check-metadata-for-schema-updates.r
```

9. Update publication endpoints if there are published packages (landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/irods-ruleset-uu/tools/update-publications.r
```
