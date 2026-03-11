---
parent: Release Notes
title: v2.0
nav_order: 88
---
# Release Notes - Yoda v2.0

Version: 2.0

Released: 6 October 2025

## What's new

### Changes affecting functionality for data stewards and researchers
- **Multi-file download**: added support for downloading multiple files and folders directly from the portal as a zip file
- **Open data package download**: added support for downloading an open data package from the landing page as a zip file
- **File browser navigation**: when searching for data objects, the browser now navigates directly to the results page where the data object is located (this does not apply to collections with a large number of data objects).
- **Keyword selector**: introduced a new tree keyword selector for use in metadata forms, supporting controlled vocabularies. It is currently used in the [EPOS-MSL metadata schema](https://github.com/UtrechtUniversity/yoda-ruleset/blob/development/schemas/epos-msl-0/metadata.json)
- **SURF Portal theme**: added a new theme for the SURF portal
- **Multiple deposit groups**: enhanced support for managing multiple deposit groups in the deposit module (previously, the deposit module supported only a single group per environment)
- **Landing page themes**: added support for technical administrators to configure a customizable theme for landing pages using the `landingpage_theme` and `landingpage_root` Ansible parameters. It works by configuring Yoda to generate landing pages that use a custom CSS file.
- **Data package archiving**: the data package archiving process will now automatically retry failed _copy to vault_ operations, which improves the reliability of this process.
- **Vault archiving workflow**: enhanced support for the [vault archiving](../design/overview/vault-archive.md) workflow
- **Secured status removal**: removed the `Secured` status from the research space
- **Intake module removal**: removed the intake module
- **Group manager**: Group managers and technical admins can now change their own role to a normal member or remove themselves from a group as long as there is another group manager in the group.

### Changes affecting technical administrators
- **Ubuntu and AlmaLinux support**: added [support](../administration/supported-distributions.md) for Ubuntu 24.04 and AlmaLinux 9
- **New admin privilege group**: introduced a new admin privilege group ([priv-admin](../design/overview/group-manager.md#how-are-the-roles-in-yoda-implemented-on-top-of-the-irods-permission-system)), which allows users to perform administrative tasks
- **Functional administration page**: added a new administration page for performing functional tasks via the portal, such as [setting a maintenance banner in the portal](../administration/setting-maintenance-banner.md)
- **Ansible library for iRODS**: added an Ansible library to modify iRODS resources
- **NFS Shares Configuration**: introduced an Ansible role for configuring NFS shares as iRODS storage resources
- **Rsyslog Support**: added support for rsyslog to log iRODS messages in a readable format
- **RADIUS fallback removal**: removed the RADIUS fallback option
- **Experimental caching**: introduced experimental support for portal view and API caching

### Other changes
- Python: update rulesets to 3.12
- iRODS: update to v4.3.4
- Python-irodsclient: update to v3.2.0
- GoCommands: update to v0.11.5
- Flask and dependencies: update to v3.1.1
- Bootstrap: update to v5.3.8
- Mailpit: update to v1.27.9

### Known issues
- Collections with single apex "'" in the name do not work ([irods/irods#5727](https://github.com/irods/irods/issues/5727))
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python ([irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54))
- Deallocation of KeyValPair results in bad AVU or error ([irods/irods#8265](https://github.com/irods/irods/issues/8265))
- Renaming collection with multi-byte characters mangles subcollection paths ([irods/irods#6239](https://github.com/irods/irods/issues/6239))

## Upgrading from previous release

### Software version requirements

The playbook requires Ansible 2.16.x or higher.

Version constraints:
- Requires Yoda external user service to be on version 1.9.x or higher.
- Requires Yoda public server to be on version 1.9.x or higher.
- Although Yoda itself supports EL 8 systems (e.g. RHEL 8) as a database server, Ansible has dropped support for EL 8 in version 2.17.0. It is recommended to use EL 9 or Ubuntu 24.04 LTS for new database servers. For existing
  EL 8 database servers, run Ansible 2.16.x in a virtual environment, and install Python 3.12 on the EL 8
  server:

```bash
sudo yum install python3.12 python3.12-pip
sudo /usr/bin/python3.12 -m pip install cryptography psycopg2-binary selinux
```

### Upgrade process

1. Backup/copy custom configurations made to Yoda version 1.9.5 / 1.10.0
To view what files were changed from the defaults, run `git diff`.

2. After ensuring the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Check out the `v2.0.4` tag of the Yoda Git repository:
```bash
git checkout v2.0.4
```

4. Set the Yoda version to `v2.0.4` in the configuration:
```yaml
yoda_version: v2.0.4
```

5. If the old configuration contained an iRODS authentication scheme setting, update it to use `pam_password`. Example:
```yaml
irods_authentication_scheme: pam_password
```

6. It is recommended to explicitly set the Ansible interpreter path in the `group_vars` (if the Yoda environment servers all
have the same Linux distribution) or in the `host_vars` (if they have different Linux distributions) in order to prevent
problems with Ansible using a different interpreter than expected.

  For EL 9 environments:
  ```yaml
  ansible_python_interpreter: /usr/bin/python3.9
  ```

  For EL 8 and Ubuntu 24.04 LTS environments (see also additional instructions above for EL 8 servers):
  ```yaml
  ansible_python_interpreter: /usr/bin/python3.12
  ```

7. Install all Ansible collections needed to deploy Yoda:
```bash
ansible-galaxy collection install -r requirements.yml
```

8. Run the Ansible playbook in check mode:
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml --check
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml --check
```

9. If the playbook has finished successfully in check mode, run the Ansible playbook normally:
```bash
ansible-playbook -i <path-to-your-environment> playbook.yml
### EXAMPLE ###
ansible-playbook -i /environments/development/allinone playbook.yml
```

10. Update publication endpoints if there are published packages (DataCite, landingpages and OAI-PMH):
```bash
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/update-publications.r
```

11. Manually restart Apache on all portal and WebDAV servers

On Ubuntu:

```bash
sudo systemctl restart apache2
```

On RHEL:

```bash
sudo systemctl restart httpd
```

12. Manually restart the portal application on all portal servers
```bash
sudo touch /var/www/yoda/yoda.wsgi /var/www/yoda/yoda_debug.wsgi
```

13. When updating from a version before v2.0.4 to v2.0.4 or later, the statistics export function
    performance improvements will become effective after completion of the first storage statistics job run
    after the upgrade. Either wait one or two days for the scheduled job to complete, or manually run a
    statistics update job after the upgrade:
```bash
/bin/irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/storage-statistics.r
```
