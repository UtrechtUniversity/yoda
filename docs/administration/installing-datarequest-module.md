---
parent: Administration Tasks
title: Installing datarequest module
nav_order: 7
---
# Installing datarequest module

## Before deployment using Ansible

### Enable the datarequest module in Ansible
Set `enable_datarequest` to `true` in configuration.
```
enable_datarequest: true
```

### Set Ansible parameters specific to the datarequest module
Users can contact a helpdesk email address for questions regarding the
datarequest procedure. Set the fields below to specify the help contact.
```
datarequest_help_contact_name: the data manager
datarequest_help_contact_email: help@yoda.instance
```

## After deployment using Ansible

### Creating and populating required groups

Ensure that the following groups exists, each with category `datarequests`,
subcategory `research` and data classification `unspecified`:
    ```
    datarequests-research-datamanagers
    datarequests-research-project-managers
    datarequests-research-data-access-committee
    ```

Instructions:

1. Log into an account on the server with permission to create new groups.

    `sudo su irods`

2. Create the groups.

    ```
    irule -r irods_rule_engine_plugin-irods_rule_language-instance 'uuGroupAdd("datarequests-research-datamanagers", "datarequest", "research", "Datamanagers", "", *status, *message);' null ruleExecOut
    irule -r irods_rule_engine_plugin-irods_rule_language-instance 'uuGroupAdd("datarequests-research-project-managers", "datarequest", "research", "Project managers", "", *status, *message);' null ruleExecOut
    irule -r irods_rule_engine_plugin-irods_rule_language-instance 'uuGroupAdd("datarequests-research-data-access-committee", "datarequest", "research", "Data Access Committee", "", *status, *message);' null ruleExecOut
    ```

3. Confirm that the groups exist.

    `iadmin lg`

Using the group manager, populate these groups with appropriate members.

### Updating the data request module schemas

If data request module schemas are already present, they will not be overwritten when the Ansible playbook is executed.

The data request module schemas can be updated by executing `/etc/irods/yoda-ruleset/tools/install-datarequest-schemas.sh $zoneName`.
