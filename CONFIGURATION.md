# Configuration
Instructions on how to configure a (new) Yoda instance.

## 1. Create new environment
This first step is optional.
You can configure a (new) Yoda instance in an existing environment or create a new environment.
A [environment](environments/development/) environment is available with two example instances.

To create a new environment make a new directory under [environment](environments/).
For example a production environment:
```bash
mkdir environments/production
```

We call our new instance 'yoda', so create a new instance directory:
```bash
mkdir environments/production/yoda
```

In this new instance directory two directories are needed, on for the Yoda instance variables (group_vars) and one for host specific variables (host_vars).
```bash
mkdir environments/production/yoda/group_vars
mkdir environments/production/yoda/host_vars
```

## 2. Add hosts of new Yoda instance

Hosts of a Yoda instance are defined in the [Ansible inventory](https://docs.ansible.com/ansible/latest/intro_inventory.html) file 'hosts'.
For the development instance 'full' this inventory can be found in [environments/development/full/hosts](environments/development/full/hosts).
In the inventory the hosts of an instance are defined, their functional roles and to which groups they belong.

Example configuration defining the and functional roles of an instance called 'yoda':
```bash
[yoda:children]
host1.yoda.dev
host2.yoda.dev
host3.yoda.dev

[yoda-portal]
host1.yoda.dev

[yoda-database]
host1.yoda.dev

[yoda-icat]
host1.yoda.dev

[yoda-resource]
host2.yoda.dev

[yoda-public]
host3.yoda.dev
```

Add the new functional roles of the instance to the corresponding groups.
For example:
```bash
[portals:children]
yoda-portal

[databases:children]
yoda-database

[icats:children]
yoda-icat

[resources:children]
yoda-resource

[publics:children]
yoda-public
```

Last step to add the hosts of a new Yoda instance is to create configuration files for every new host.
In development environment these configuration files are placed in [environments/development/hosts](environments/development/host_vars).
For example, for host 'host1.yoda.dev' a configuration file is created:
```bash
touch environments/development/host_vars/host1.yoda.dev
```

And place the basic host configuration in the new file:
```bash
---
ansible_host: host1.yoda.dev
```

## 3. Configure (new) Yoda instance
To configure a (new) Yoda instance we have to edit the instance configuration in the Yoda instance variables directory (group_vars).
In case of a new Yoda instance we can copy a [configuration](environments/development/full/group_vars/full.yml) of a development instance as base.

### Ansible configuration
Fill in the administrative user on the Yoda instance for Ansible 'ansible_user' and the location of the private key file of this administrative user 'ansible_ssh_private_key_file'.
If these users and/or private key file is different for each host then define these in the corresponding host specific variables (host_vars).

### Yoda configuration
Fill in the name of the Yoda instance 'instance', the version you want to deploy 'yoda_version', the Yoda Portal fully qualified domain name 'yoda_portal_fqdn' and  Yoda Davrods WebDAV fully qualified domain name 'yoda_davrods_fqdn'.

### iRODS configuration
Set iRODS admin username 'irods_admin' / password 'irods_password' and iRODS database username 'irods_database_user' / password 'irods_database_password'.
Set the name of the iRODS zone 'irods_zone' and the fully qualified domain names of the icat server 'irods_icat_fqdn', database server 'irods_database_fqdn' and resource server 'irods_resource_fqdn'.
Finish iRODS configuration by defining the default resource name 'irods_default_resc' and resource configuration 'irods_resources'.
