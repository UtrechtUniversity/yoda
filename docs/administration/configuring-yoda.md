---
parent: Administration Tasks
title: Configuring Yoda
nav_order: 0
---
# Configuring Yoda
Instructions on how to configure a (new) Yoda instance.

## 1. Create new environment
This first step is optional.
You can configure a (new) Yoda instance in an existing environment or create a new environment.
A `development` environment is available with two example instances.

To create a new environment make a new directory under `environments`.
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
For the development instance 'full' this inventory can be found in `environments/development/full/hosts`.
In the inventory the hosts of an instance are defined, their functional roles and to which groups they belong.

Example configuration defining the and functional roles of an instance called 'yoda':
```bash
[yoda:children]
yoda_portal
yoda_database
yoda_icat
yoda_resource
yoda_public
yoda_eus

[yoda_portal]
host1.yoda.test

# leave this out when using an existing database for ICAT
[yoda_database]
host1.yoda.test

[yoda_icat]
host1.yoda.test

[yoda_resource]
host2.yoda.test

[yoda_public]
host3.yoda.test

[yoda_eus]
host4.yoda.test
```

Add the new functional roles of the instance to the corresponding groups.
For example:
```bash
[portals:children]
yoda_portal

# leave this out when using an existing database for ICAT
[databases:children]
yoda_database

[icats:children]
yoda_icat

[resources:children]
yoda_resource

[publics:children]
yoda_public

[eus:children]
yoda_eus
```

It is possible to deploy davrods to a separate host by adding a davrods host and group:
```bash
[yoda:children]
yoda_portal
yoda_davrods
yoda_database
yoda_icat
yoda_resource
yoda_public
yoda_eus

[yoda_davrods]
host5.yoda.test

[davrods:children]
yoda_davrods
```

Last step to add the hosts of a new Yoda instance is to create configuration files for every new host.
In development environment these configuration files are placed in `environments/development/hosts`.
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
In case of a new Yoda instance we can copy a configuration of a full development (`environments/development/full/`) instance as base.
The configuration is split in several parts. Below an overview of these parts and the configuration options available.

### Ansible configuration

Variable   | Description
-----------|---------------------------------------------
ansible_user                 | Administrative user on instance for Ansible
ansible_ssh_private_key_file | Path to private key file of administrative user
repo_only                    | Only download packages from repos

Note: if one of these variables are different for a host then define them in the corresponding host specific variables file (host_vars).

### Yoda configuration

Variable   | Description
-----------|---------------------------------------------
instance                     | Name of Yoda instance, as defined in hosts file
yoda_version                 | Git branch, for example: development or release-0.9.7
yoda_environment             | Yoda environment: development, testing, acceptance or production
yoda_portal_fqdn             | Yoda Portal fully qualified domain name (FQDN)
yoda_davrods_fqdn            | Yoda Davrods WebDAV fully qualified domain name (FQDN)
yoda_davrods_anonymous_fqdn  | Yoda Davrods anonymous WebDAV fully qualified domain name (FQDN)
yoda_davrods_logo_path       | Path of the DavRODS logo on the portal. Defaults to the themed logo.
yoda_davrods_logo_link       | URL that the DavRODS logo is linked to (default:  https://www.uu.nl)
yoda_enable_httpd            | Whether to enable the httpd service (boolean, default value: true). Set to false if manual actions are needed before starting the web server (e.g. mounting encrypted volumes)
httpd_log_forwarded_for      | Whether to log X-Forwarded-For headers in Apache logs (boolean, default value: false). This logs source IP addresses of requests if requests to the Yoda web portal and/or WebDAV interface are routed via a load balancer.
httpd_log_user_agent         | Whether to log the user agent of browsers and WebDAV clients in the Apache logs (boolean, default value: false)
tcp_keepalive_time           | IPv4 TCP keepalives: time until first keepalive (kernel parameter). Can be useful to tune in order to prevent timeouts on long transfers.
tcp_keepalive_intvl          | IPv4 TCP keepalives: time between keepalives (kernel parameter). Can be useful to tune in order to prevent timeouts on long transfers.

### iRODS configuration

Variable                     | Description
-------------------------------------|---------------------------------
irods_admin                          | iRODS admin username
irods_password                       | iRODS admin password
irods_database_user                  | The iRODS database username
irods_database_password              | The password for the iRODS database username
irods_database_enable_yoda_indexes   | Enable indexes to speed up Yoda search operations (default: false). This is mainly useful for medium-sized and large environments (millions of data objects or more). Please note that the indexes can take up a significant amount of diskspace (rough estimate: 10-30% increase in database size). They will be created asynchronously. This can take some time on existing environments with a significant amount of data, and temporarily decrease performance.
irods_zone                           | The name of the iRODS Zone
irods_icat_fqdn                      | iRODS iCAT fully qualified domain name (FQDN)
irods_database_fqdn                  | iRODS database fully qualified domain name (FQDN)
irods_resource_fqdn                  | iRODS resource fully qualified domain name (FQDN). Don't define this variable if you have multiple resource servers.
irods_default_resc                   | iRODS default resource name
irods_resc_trigger_pol               | List of text patterns for matching non-primary resources where changes also need to trigger policies (e.g. asynchronous replication). Example: ["^testResc$","^myResc$"]
irods_ssl_verify_server              | Verify TLS certificate, use 'cert' for acceptance and production
irods_resources                      | Definition of iRODS resources of this Yoda instance
irods_service_type                   | Possible values: 'sysv' (System V) or 'systemd'
irods_max_open_files                 | Maximum number of open files for iRODS service (only effective when irods_service_type is set to 'systemd')
irods_enable_service                 | Whether to enable the iRODS service. Set to false if manual actions are needed before starting iRODS, e.g. mounting encrypted volumes (only effective when irods_service_type is set to 'systemd')
irods_rum_job_enabled                | Whether to enable the daily RUM job for removing unused metadata entries (default: true)
irods_rum_job_hour                   | Time to run RUM job - hour (default: 20)
irods_rum_job_minute                 | Time to run RUM job - minute (default: 0)

### Research module configuration

Variable   | Description
-----------|---------------------------------------------
default_yoda_schema          | Default Yoda XML scheme: default-0 or default-1
enable_revisions             | Enable revisions: yes (1) or no (0)
enable_async_replication     | Enable asynchronous replication cronjob: yes (1) or no (0)
revision_strategy            | Revision strategy: A, B, J or Simple
yoda_random_id_length        | Length of random ID to add to persistent identifier
yoda_prefix                  | Prefix for internal portion of persistent identifier
update_rulesets              | Update already installed rulesets with git
override_resc_install_rulesets | Install rulesets on server even if it is a resource server (default: false). This override parameter can be used on resource servers that have an additional role, e.g. DavRODS server
update_schemas               | Update already installed schemas, formelements and stylesheets: yes (1) or no (0)
credential_files             | Location of Yoda credentials files
temporary_files              | List of temporary files for cleanup functionality

### Deposit module configuration

Variable                     | Description
-----------------------------|---------------------
enable_deposit               | Enable deposit module

### Intake module configuration

Variable                     | Description
-----------------------------|---------------------
enable_intake                | Enable intake module
intake_groups                | List of intake groups (without the "grp-intake-" prefix)
intake_extended_timeout      | If the intake module is enabled, portal iRODS session timeouts and portal VHost timeouts will be changed to this value (in seconds), in order to be able to handle long synchronous operations, such as intake scans (default: 1800)

### Datarequest module configuration

Variable                       | Description
-------------------------------|---------------------
enable_datarequest             | Enable datarequest module
datarequest_help_contact_name  | Help contact name
datarequest_help_contact_email | Help contact email address

### OpenSearch configuration

Variable                       | Description
-------------------------------|---------------------
enable_open_search             | Enable OpenSearch and indexing plugin
opensearch_server              | FQDN of the OpenSearch server (typically the provider)

### Yoda notifications configuration

Variable                     | Description
-----------------------------|---------------------------------------------
send_notifications           | Enable notifications: yes (1) or no (0)
notifications_sender_email   | Notifiations sender email address
notifications_reply_to       | Notifiations Reply-To email address

### Yoda internal SMTP settings configuration

Variable                     | Description
-----------------------------|---------------------------------------------
smtp_server                  | SMTP server to send mail to
smtp_username                | SMTP server username
smtp_password                | SMTP server password
smtp_auth                    | Whether to use SMTP authentication (true/false, default: true)
smtp_starttls                | Whether to force StartTLS on non-SMTP connections (true/false, default: true)

### PostgreSQL database configuration

Variable                               | Description
---------------------------------------|---------------------------------------------
postgresql_max_connections             | Maximum number of database connections (default: 100)
postgresql_shared_buffers              | Amount of memory database should use for shared buffers. Rule of thumb: set to 25% of memory on dedicated database server; on a shared server, it should probably be lower. Default value: 32 MB.
postgresql_work_mem                    | Maximum amount of worker memory. Rule of thumb: increasing worker memory can help with improving performance, but it is necessary to ensure that sufficient memory is available, considering the maximum number of database connections. Default value: 1 MB.
postgresql_maintenance_work_mem        | Maximum amount of memory for maintenance processes, such as VACUUM. Default value: 16 MB.
postgresql_effective_cache_size        | Tells the query planner how much memory it can expect to be available for disk caching for the database. Rule of thumb: set to approximately 50-75% on dedicated database server. Default value: 128 MB.
postgresql_random_page_cost            | Tells the query planner about the relative cost of random access versus sequential access. You could use a tool like fio to get an estimate, or use a ballpark estimate based on the type of storage of the database volume (e.g. 1.0 for SSD-based storage). Default value is 4.0.
postgresql_log_line_prefix:            | Format of log message prefix in the PostgreSQL log, for adding timestamps etc. to log messages. The default value adds a timestamp and process number, which is sufficient for most purposes. It might be useful to log additional information in specific situations, such as when troubleshooting database issues.
postgresql_log_min_duration_statement  | Minimum number of milliseconds for slow query logging (default: -1 / disabled)
postgresql_log_autovacuum_min_duration | Minimum number of milliseconds for logging slow autovacuum actions (default: -1 / disabled)
postgresql_timezone                    | Timezone that PostgreSQL uses. Defaults to Europe/Amsterdam.

### PgBouncer configuration

Variable                                     | Description
---------------------------------------------|---------------------------------------------
enable_pgbouncer                             | Whether to enable PgBouncer (default: false)
pgbouncer_pool_mode                          | Specifies when a server connection can be reused by other clients (default: session)
pgbouncer_max_client_conn                    | Maximum number of client connections allowed (default: 200)
pgbouncer_default_pool_size                  | How many server connections to allow per user/database pair (default: 50) 
pgbouncer_reserve_pool_size                  | How many additional connections to allow to a pool (default: 25) 
pgbouncer_reserve_pool_timeout               | If a client has not been serviced in this time, use additional connections from the reserve pool (default: 2)
pgbouncer_override_ignore_startup_parameters | Adjust ignore_startup_parameters setting of PGbouncer (default: undefined / use OS default value)

### Postfix configuration

Variable                     | Description
-----------------------------|---------------------------------------------
enable_postfix               | Whether to enable the Postfix local MTA (default: false)
postfix_myhostname           | Hostname of server where Postfix will be installed (compulsory parameter if Postfix is enabled)
postfix_relayhost            | Relay host, the server that Postfix should send emails to (compulsory parameter if Postfix is enabled)
postfix_relayhost_port       | Port of relay host (default: 587)
postfix_relayhost_username   | User name for authentication on relay host (compulsory parameter if Postfix is enabled)
postfix_relayhost_password   | Password for authentication on relay host (compulsory parameter if Postfix is enabled)
postfix_smtp_enable_tls      | Whether to enable TLS on connections to relay host. This also enables authentication on connections to the relay host (default: true)
postfix_enable_debugging     | This enables additional logging on connections to the relay host. Useful for troubleshooting. (default: false)
postfix_myorigin             | Sets origin domain for emails sent on the system. Defaults to the postfix_myhostname domain.
postfix_inet_protocols       | Refers to Postfix inet_protocols setting. Can be useful for running Postfix in IPv4 only mode, if no IPv6 connectivity is available (default: "all")
postfix_canonical_map        | An optional dictionary of rewrite rules for email addresses. See [the local Postfix MTA page](local-postfix-mta.md) for further information.

### DataCite Configuration

Variable                     | Description
-----------------------------|---------------------------------------------
datacite_username            | DataCite username
datacite_password            | DataCite password
datacite_prefix              | DataCite DOI prefix
datacite_rest_api_url        | DataCite REST API URL

### EPIC PID Configuration

Variable                     | Description
-----------------------------|---------------------------------------------
epic_url                     | EPIC PID server URI (undefined disables EPIC PID)
epic_handle_prefix           | EPIC PID prefix
epic_key                     | EPIC PID key (base64 encoded)
epic_cert                    | EPIC PID cert (base64 encoded)

### Data Access Tokens configuration

Variable                | Description
------------------------|------------------------------------
enable_tokens           | Boolean indicating if Data Access Tokens for webDAV and iCommands are enabled. Must be `true` or `false`
token_database          | Location of the database that contain the tokens
token_database_password | Token database password
token_length            | Length of data access tokens
token_lifetime          | Lifetime of data access tokens (in hours) (in hours)
enable_radius_fallback  | Fall back on RADIUS authentication if token authentication fails (default: false). Only enables RADIUS fallback if `enable_tokens` is set to `true`.This is a legacy parameter that will be removed in a future version of Yoda.

### Public host configuration

Variable                     | Description
-----------------------------|---------------------------------------------
yoda_public_host             | Yoda public host
yoda_public_fqdn             | Yoda public fully qualified domain name (FQDN)
upload_priv_key              | Yoda public upload private key (base64 encoded)
upload_pub_key               | Yoda public upload public key (base64 encoded)

### External user service configuration

Variable                     | Description
-----------------------------|---------------------------------------------
yoda_eus_fqdn                | Yoda External User Service fully qualified domain name (FQDN)
eus_api_fqdn                 | External User Service API fully qualified domain name (FQDN)
eus_api_port                 | External User Service API port
eus_api_secret               | External User Service API secret
eus_db_password              | External User Service database password
eus_smtp_host                | External User Service SMTP host
eus_smtp_port                | External User Service SMTP port
eus_smtp_user                | External User Service SMTP user
eus_smtp_password            | External User Service SMTP password
eus_smtp_auth                | External User Service SMTP authentication (true/false, default: true)
eus_smtp_security            : External User Service SMTP encryption (tls/ssl/false, default: tls)
eus_smtp_from_address        | External User Service from address
eus_smtp_replyto_address     | External User Service replyto address
eus_mail_template            | External User Service mail template

### OpenID Connect (OIDC) configuration

Variable   | Description
-----------|---------------------------------------------
oidc_active         | Boolean indicating whether OpenId Connect with the following parameters is enabled of not. Must be `true` or `false`
oidc_domains        | Domains that should use OIDC (list). If this parameter is set, the first domain in the list is also used to generate the user name placeholder on the portal gate and login pages.
oidc_client_id		| OIDC Client Id
oidc_client_secret	| OIDC Client Secret/Password
oidc_callback_url   | OIDC Callback url
oidc_auth_base_uri	| OIDC Authorization URI without parameters
oidc_login_hint     | Boolean indicating whether login hint should be added to Authorization URI (default: True)
oidc_token_uri		| OIDC Token URI
oidc_userinfo_uri	| OIDC Userinfo URI
oidc_scopes         | OIDC Scopes
oidc_acr_values		| OIDC Authentication Context Class Reference Values
oidc_email_field	| The identifier of the JSON field in the `id_token` containing the email address. Default: `email` the email address (default: email)
oidc_jwks_uri       | The url where the JWKS can be found (Java web key sets)
oidc_jwt_issuer     | The issuer of the JWT tokens ('iss' value in JWT, for verification)
oidc_req_exp        | Check that exp (expiration) claim is present
oidc_req_iat        | Check that iat (issued at) claim is present
oidc_req_nbf        | Check that nbf (not before) claim is present
oidc_verify_aud     | Check that aud (audience) claim matches audience
oidc_verify_iat     | Check that iat (issued at) claim value is an integer
oidc_verify_exp     | Check that exp (expiration) claim value is OK
oidc_verify_iss     | Check that iss (issue) claim is as expected

### Mailpit configuration

Variable                 | Description
-------------------------|---------------------------------------------
enable_mailpit           | Enable [Mailpit](https://github.com/axllent/mailpit) for email testing. Should only be enabled on local development environments for security reasons. Mailpit and Postfix shouldn't be enabled simultaneously. Default: false
mailpit_version          | Mailpit version to install
mailpit_max_messages     | Maximum number of messages to store (default: 10000)
mailpit_smtp_bind_address| Address to bind on for SMTP interface (default: 0.0.0.0)
mailpit_smtp_port        | TCP port for SMTP interface (default: 25)
