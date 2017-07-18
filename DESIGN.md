Design
======

Content Organization
--------------------
Our Ansible playbook for automated deployment of YoDa is organised like this:
environments/
   development/
      hosts               # inventory file for development environment
      group_vars/
         group1           # here we assign variables to particular groups
         group2           # ""
      host_vars/
         hostname1       # if systems need specific variables, put them here
         hostname2       # ""

   testing/
      hosts               # inventory file for testing environment
      group_vars/
         group1           # here we assign variables to particular groups
         group2           # ""
      host_vars/
         hostname1       # if systems need specific variables, put them here
         hostname2       # ""

   acceptance/
      hosts               # inventory file for acceptance environment
      group_vars/
         group1           # here we assign variables to particular groups
         group2           # ""
      host_vars/
         hostname1       # if systems need specific variables, put them here
         hostname2       # ""

   production/
      hosts               # inventory file for production environment
      group_vars/
         group1           # here we assign variables to particular groups
         group2           # ""
      host_vars/
         hostname1        # if systems need specific variables, put them here
         hostname2        # ""

playbook.yml              # master playbook

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
        vars/             #
            main.yml      #  variables associated with this role
        defaults/         #
            main.yml      #  default lower priority variables for this role
        meta/             #
            main.yml      #  role dependencies

    apache/               # same kind of structure as "common" was above, done for the apache role
    composable-resources/ # ""
    hostentries/          # ""
    irods-database/       # ""
    irods-icat/           # ""
    irods-icommands/      # ""
    irods-microservices/  # ""
    irods-resource/       # ""
    irods-runtime/        # ""
    php/                  # ""
    postgresql/           # ""
    yoda-davrods/         # ""
    yoda-portal/          # ""
    yoda-rulesets/        # ""

Master Playbook
---------------
The master [playbook](playbook.yml) consists of four tiers:
* portal
* database
* iCAT
* resource

### portal tier
The portal tier provisions the host with the following:
* Apache webserver
* PHP
* iRODS iCommands & runtime
* YoDa portal and davrods

### database tier
The portal tier provisions the host with the following:
* PostgreSQL database
* iRODS database plugin

### iCAT tier
The portal tier provisions the host with the following:
* iRODS iCAT server & runtime
* iRODS microservices
* YoDa rulesets

### resource tier
The portal tier provisions the host with the following:
* iRODS resource server & runtime
* iRODS microservices
* YoDa rulesets
