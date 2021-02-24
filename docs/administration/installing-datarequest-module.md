# Installing datarequest module

## Before deployment using Ansible

### Enable the datarequest module in Ansible
Set `enable_datarequest` to `true` in configuration.
```
enable_datarequest: true
```

Add the `yoda-portal-datarequest` repository to `extra_modules`.
```
extra_modules:
  - name: datarequest
    repo: "https://github.com/UtrechtUniversity/yoda-portal-datarequest.git"
    dest: /var/www/yoda/yoda-portal/modules/datarequest
    version: "\{\{ yoda_version \}\}"
```

## After deployment using Ansible

### Creating and populating required groups

Ensure that the following groups exists, each with category `datarequests`,
subcategory `research` and data classification `unspecified`:
    ```
    datarequests-research-datamanagers
    datarequests-research-board-of-directors
    datarequests-research-data-management-committee
    ```

Instructions:

1. Log into an account on the server with permission to create new groups.

    `sudo su irods`

2. Create the groups.

    ```
    irule -r irods_rule_engine_plugin-irods_rule_language-instance 'uuGroupAdd("datarequests-research-datamanagers", "datarequest", "research", "Datamanagers", "", *status, *message);' null ruleExecOut
    irule -r irods_rule_engine_plugin-irods_rule_language-instance 'uuGroupAdd("datarequests-research-board-of-directors", "datarequest", "research", "Board of Directors", "", *status, *message);' null ruleExecOut
    irule -r irods_rule_engine_plugin-irods_rule_language-instance 'uuGroupAdd("datarequests-research-data-management-committee", "datarequest", "research", "Data Management Committee", "", *status, *message);' null ruleExecOut
    ```

3. Confirm that the groups exist.

    `iadmin lg`

Using the group manager, populate these groups with appropriate members.

### Customizing and installing schemas
For a fully functional datarequest module, schemas for the various forms have to
be present. A set of templates for these schemas can be found in the
`irods-ruleset-uu` repository in the `datarequest/schemas` directory. These meet
the requirements of the datarequest procedure of
[the YOUth cohort study](https://www.uu.nl/en/research/youth-cohort-study).

For a production deployment to a Yoda instance for which these templates are
suitable as is (e.g. the Yoda instance of YOUth), only one template has to be
changed, and that is `datarequest/schemas/youth-0/assignment/schema.json`.
Within this template, replace the example DMC member entries in the `assign_to`
section with real entries. The `enum` field should be an array of usernames of
the DMC members and the `enumNames` field should be an array with corresponding
"display names" (which are visible in the assignment form).

Instructions:

1. Copy the template to a temporary directory for adjustment.

    ```bash
    cp datarequest/schemas/youth-0/assignment/schema.json /tmp/
    ```

2. Edit the template (see explanation above).

3. Overwrite the default assignment schema with the edited schema.

    ```bash
    iput -f /tmp/schema.json /IRODS_ZONENAME_HERE/yoda/datarequest/schemas/youth-0/assignment/schema.json
    ```

### Customizing the helpdesk email address
Users can contact a helpdesk email address for questions regarding the
datarequest procedure. This address is configured in `config/config.php` of the
`yoda-portal-datarequest` repository by setting the `help_contact_name` and
`help_contact_email` fields.

Instructions:

1. Adjust the above-mentioned fields in `/var/www/yoda/yoda-portal/modules/datarequest/config/config.php`.
