---
parent: Release Notes
title: v2.2
nav_order: 87
---
# Release Notes - Yoda v2.2

Version: 2.2

Released: TBA

## What's new

### Changes affecting functionality for data stewards and researchers
-

### Changes affecting technical administrators
-

### Other changes
- GoCommands: update to v0.12.4
- Mailpit: update to v1.31.1

### Known issues
- Deadlock in msiDataObjRepl & msiDataObjCopy when called from Python ([irods/irods_rule_engine_plugin_python#54](https://github.com/irods/irods_rule_engine_plugin_python/issues/54))

## Upgrading from previous release

### Software version requirements

The playbook requires Ansible 2.16.x or higher.

Version constraints:
- Requires Yoda external user service to be on version 2.1.x or higher.
- Requires Yoda public server to be on version 2.1.x or higher.

### Upgrade process

1. Backup/copy custom configurations made to Yoda version 2.1.x
To view what files were changed from the defaults, run `git diff`.

2. After ensuring the configurations are stored safely in another folder, reset the Yoda folder using `git stash` or when you want to delete all changes made: `git reset --hard`.

3. Check out the `development` tag of the Yoda Git repository:
```bash
git checkout development
```

4. Set the Yoda version to `development` in the configuration:
```yaml
yoda_version: development
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

    For Ubuntu 24.04 LTS environments:
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

11. Manually restart Apache on all portal and WebDAV servers,
example:

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
