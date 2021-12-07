---
grand_parent: Software Design
parent: System Overview
nav_order: 11
---

# Deployment

## Ansible Playbook
The master playbook for automated deployment of Yoda can be found in [playbook.yml](https://github.com/UtrechtUniversity/yoda/playbook.yml).
It consists of four tier which implements four distinct functional roles:
* Yoda webportal
* iRODS database
* iRODS provider (catalog) server
* iRODS consumer (resource) server

### Yoda webportal tier
The Yoda webportal tier provisions the host with the following:
* Apache webserver
* Python
* iRODS iCommands & runtime
* Yoda portal and davrods

### iCAT database tier
The iCAT database tier provisions the host with the following:
* PostgreSQL database
* iRODS database plugin

### iCAT server
The iCAT server tier provisions the host with the following:
* iRODS iCAT server & runtime
* iRODS microservices
* iRODS resource configuration
* Yoda ruleset

### iRODS resource server
The iRODS resource server tier provisions the host with the following:
* iRODS resource server & runtime
* iRODS microservices
* Yoda ruleset

Roles
-----
All the roles can be found in the roles directory using the following content organization:
```
roles/
    common/               # this hierarchy represents a "role"
        tasks/            #
            main.yml      # tasks file can include smaller files if warranted
        handlers/         #
            main.yml      # handlers file
        templates/        # files for use with the template resource
            ntp.conf.j2   # templates end in .j2
        files/            #
            bar.txt       #  files for use with the copy resource
            foo.sh        #  script files for use with the script resource
        defaults/         #
            main.yml      #  default variables for this role
        meta/             #
            main.yml      #  role dependencies

    apache/               # same kind of structure as "common" was above, done for the apache role
    certificates/         # ""
    composable-resources/ # ""
    hostentries/          # ""
    irods-database/       # ""
    irods-icat/           # ""
    irods-icommands/      # ""
    irods-microservices/  # ""
    irods-resource/       # ""
    irods-runtime/        # ""
    postgresql/           # ""
    python-irodsclient/   # ""
    python3/              # ""
    yoda-davrods/         # ""
    yoda-landingpages/    # ""
    yoda-moai/            # ""
    yoda-portal/          # ""
    yoda-rulesets/        # ""
    yoda-test/            # used in the test.yml playbook
    yoda-zabbixagent      # used in the zabbix.yml playbook
    yoda-zabbixdatabase   # used in the zabbix.yml playbook
    yoda-zabbixyodaitems  # used in the zabbix.yml playbook
```


## Environments
The playbook can be used with different environments.
Each environment has its own inventory (hosts) with all instances.
Each instance is configured in group variables (group_vars).
Host specific variables (host_vars) may exist for each host.
```
environments/
   development/
      allinone/
         hosts             # inventory file for allinone instance
         group_vars/
            allinone.yml   # here we assign variables to particular groups
         host_vars/
            combined       # if systems need specific variables, put them here
      full/
         hosts             # inventory file for full instance
         group_vars/
            full.yml       # here we assign variables to particular groups
         host_vars/
            portal         # if systems need specific variables, put them here
            database       # ""
            icat           # ""
            resource       # ""
            public         # ""

   testing/
      instance/
         hosts             # inventory file for testing environment
         group_vars/
            instance.yml   # here we assign variables to particular groups
         host_vars/
            hostname1      # if systems need specific variables, put them here
            hostname2      # ""

   acceptance/
      instance/
         hosts             # inventory file for acceptance environment
         group_vars/
            instance.yml   # here we assign variables to particular groups
         host_vars/
            hostname1      # if systems need specific variables, put them here
            hostname2      # ""

   production/
      instance/
         hosts             # inventory file for production environment
         group_vars/
            instance.yml   # here we assign variables to particular groups
         host_vars/
            hostname1      # if systems need specific variables, put them here
            hostname2      # ""
```
