# Configuration
Instructions on how to configure a (new) Yoda instance.

## 1. Create new environment
This first step is optional.
You can configure a (new) Yoda instance in an existing environment or create a new environment.
A [development](environments/development/) environment is available with two example instances.

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
host1.yoda.test
host2.yoda.test
host3.yoda.test

[yoda-portal]
host1.yoda.test

# leave this out when using an existing database for ICAT
[yoda-database]
host1.yoda.test

[yoda-icat]
host1.yoda.test

[yoda-resource]
host2.yoda.test

[yoda-public]
host3.yoda.test
```

Add the new functional roles of the instance to the corresponding groups.
For example:
```bash
[portals:children]
yoda-portal

# leave this out when using an existing database for ICAT
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
For example, for host 'host1.yoda.test' a configuration file is created:
```bash
touch environments/development/host_vars/host1.yoda.test
```

And place the basic host configuration in the new file:
```bash
---
ansible_host: host1.yoda.test
```

## 3. Configure (new) Yoda instance
To configure a (new) Yoda instance we have to edit the instance configuration in the Yoda instance variables directory (group_vars).
In case of a new Yoda instance we can copy a [configuration](environments/development/full/group_vars/full.yml) of a development instance as base.
The configuration is split in several parts. Below an overview of these parts and the configuration options available.

### Ansible configuration
Variable                     | Description                                     |
-----------------------------|-------------------------------------------------|
ansible_user                 | Administrative user on instance for Ansible     |
ansible_ssh_private_key_file | Path to private key file of administrative user |
repo_only                    | Only download packages from repos               |

Note: if one of these variables are different for a host then define them in the corresponding host specific variables file (host_vars).

### Yoda configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
instance                     | Name of Yoda instance, as defined in hosts file                         |
yoda_version                 | Git branch, for example: development or release-0.9.7                   |
yoda_environment             | Yoda environment: development, testing, acceptance or production        |
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
irods_zone                   | The name of the iRODS Zone                                              |
irods_icat_fqdn              | iRODS iCAT fully qualified domain name (FQDN)                           |
irods_database_fqdn          | iRODS database fully qualified domain name (FQDN)                       |
irods_resource_fqdn          | iRODS resource fully qualified domain name (FQDN)                       |
irods_default_resc           | iRODS default resource name                                             |
irods_ssl_verify_server      | Verify TLS certificate, use 'cert' for acceptance and production        |
irods_resources              | Definition of iRODS resources of this Yoda instance                     |

### Research module configuration
Variable                     | Description                                                                       |
-----------------------------|-----------------------------------------------------------------------------------|
default_yoda_schema          | Default Yoda XML scheme: default or test                                          |
enable_revisions             | Enable revisions: yes (1) or no (0)                                               |
revision_strategy            | Revision strategy: A, B, J or Simple                                              |
yoda_random_id_length        | Length of random ID to add to persistent identifier                               |
yoda_prefix                  | Prefix for internal portion of persistent identifier                              |
update_rulesets              | Update already installed rulesets with git                                        |
update_schemas               | Update already installed schemas, formelements and stylesheets: yes (1) or no (0) |
credential_files             | Location of Yoda credentials files                                                |

### Mail notifications
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
send_notifications           | Enable notifications: yes (1) or no (0)
notifications_sender_email   | Notifiations sender email address
notifications_reply_to       | Notifiations Reply-To email address
smtp_server                  | SMTP server to send mail to
smtp_username                | SMTP server username
smtp_password                | SMTP server password

### DataCite Configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
datacite_username            | DataCite username                                                       |
datacite_password            | DataCite password                                                       |
datacite_prefix              | DataCite DOI prefix                                                     |
datacite_server              | DataCite server URI                                                     |

### EPIC PID Configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
epic_url                     | EPIC PID server URI (undefined disables EPIC PID)                       |
epic_handle_prefix           | EPIC PID prefix                                                         |
epic_key                     | EPIC PID key (base64 encoded)                                           |
epic_cert                    | EPIC PID cert (base64 encoded)                                          |

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

### External user service configuration
Variable                     | Description                                                             |
-----------------------------|-------------------------------------------------------------------------|
yoda_eus_fqdn                | Yoda External User Service fully qualified domain name (FQDN)           |
eus_api_secret               | External User Service API secret                                        |
eus_db_password              | External User Service database password                                 |
eus_smtp_host                | External User Service SMTP host                                         |
eus_smtp_port                | External User Service SMTP port                                         |
eus_smtp_user                | External User Service SMTP user                                         |
eus_smtp_password            | External User Service SMTP password                                     |
eus_smtp_from_address        | External User Service from address                                      |
eus_smtp_replyto_address     | External User Service replyto address                                   |
eus_mail_template            | External User Service mail template                                     |
