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
The configuration isplit in several parts. Below an overview of these parts and the configuration options available.

### Ansible configuration
Variable                     | Description                                     |
-----------------------------|-------------------------------------------------|
ansible_user                 | Administrative user on instance for Ansible     |
ansible_ssh_private_key_file | Path to private key file of administrative user |

Note: if one of these variables are different for a host then define them in the corresponding host specific variables file (host_vars).

### Yoda configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
instance                     | Name of Yoda instance, as defined in hosts file                         |
yoda_version                 | Git branch, for example: development or release-0.9.7                   |
codeigniter_environment      | CodeIgniter environment: development, testing, acceptance or production |
yoda_portal_fqdn             | Yoda Portal fully qualified domain name (FQDN)                          |
yoda_davrods_fqdn            | Yoda Davrods WebDAV fully qualified domain name (FQDN)                  |
yoda_davrods_anonymous_fqdn  | Yoda Davrods anonymous WebDAV fully qualified domain name (FQDN)        |

### iRODS configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
irods_admin                  | iRODS admin username                                                    |
irods_password               | iRODS admin password                                                    |
irods_database_user          | The iRODS database username                                             |
irods_database_password      | The password for the iRODS database username                            |
irods_authentication_scheme  | iRODS authentication method: "Native" or "PAM"                          |
irods_zone                   | The name of the iRODS Zone                                              |
irods_icat_fqdn              | iRODS iCAT fully qualified domain name (FQDN)                           |
irods_database_fqdn          | iRODS database fully qualified domain name (FQDN)                       |
irods_resource_fqdn          | iRODS resource fully qualified domain name (FQDN)                       |
irods_default_resc           | iRODS default resource name                                             |
irods_resources              | Definition of iRODS resources of this Yoda instance                     |

### Research module configuration
Variable                     | Description                                                                       |
-----------------------------|-----------------------------------------------------------------------------------|
default_yoda_schema          | Default Yoda XML scheme: ilab or dc                                               |
enable_revisions             | Enable revisions: yes (1) or no (0)                                               |
revision_strategy            | Revision strategy: A, B, J or Simple                                              |
yoda_random_id_length        | Length of random ID to add to persistent identifier                               |
yoda_prefix                  | Prefix for internal portion of persistent identifier                              |
update_rulesets              | Update already installed rulesets with git                                        |
update_schemas               | Update already installed schemas, formelements and stylesheets: yes (1) or no (0) |

### DataCite Configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
datacite_username            | DataCite username                                                       |
datacite_password            | DataCite password                                                       |
datacite_prefix              | DataCite DOI prefix                                                     |
datacite_server              | DatacCite server URI                                                     |

### PAM Radius configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
pam_radius_config:           | server, shared secret, timeout (s)                                      |

### Public host configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
yoda_public_host             | Yoda public host                                                        |
yoda_public_fqdn             | Yoda public fully qualified domain name (FQDN)                          |
upload_priv_key              | Yoda public upload private key (base64 encoded)                         |
upload_pub_key               | Yoda public upload public key (base64 encoded)                          |
