---
parent: Administration Tasks
title: Upgrading PostgreSQL
nav_order: 11
---

# Upgrading PostgreSQL

This page has information about how to upgrade the PostgreSQL database in Yoda to a newer version.

## Background

Yoda uses PostgreSQL, an open source relational database system, as the iRODS internal database (iCAT database),
and for storing External User Service (EUS) data.

Yoda versions up to and including 1.8.6 work with PostgreSQL 9.2. Yoda 1.8.7 and later 1.8.x versions work with PostgreSQL
9.2 by default, with an optional upgrade to PostgreSQL 15. Yoda 1.9 uses PostgreSQL 15 by default. Although Yoda 1.9
should work with PostgreSQL 9.2, it is recommended to upgrade to PostgreSQL 15 either before/during the upgrade to Yoda 1.9, or
immediately afterwards.

## Upgrade methods

Existing Yoda environments can be upgraded to PostgreSQL 15 by either starting the upgrade from Ansible, or by dumping and restoring
the database manually onto a new server.

Regardless of which method you choose, the following advice applies:
- Ensure that that you have a recent database backup before starting the upgrade process.
- First perform the upgrade process on an (acceptance) test environment that resembles your production
  environments. This also helps with estimating how much time and diskspace you will need for upgrading the
  production environment.
- A database upgrade is a good opportunity to review the Yoda [configuration parameters](configuring-yoda.md) for
  PostgreSQL, and to see if any improvements can be made in areas such as performance tuning.

## Upgrading the database using Ansible

The Ansible playbook contains an option for upgrading the database automatically. Note that upgrading the database may
take a significant time on large environments.

In Yoda 1.8.7 and later 1.8.x versions, use the following configuration parameters:

```yaml
enable_pgbouncer: true
postgresql_use_native_packages: false
pgsql_version: 15

postgresql_perform_db_upgrade: true
postgresql_remove_old_data_after_upgrade: false
```

In Yoda 1.9.x, use just the following configuration parameters:

```yaml
postgresql_perform_db_upgrade: true
postgresql_remove_old_data_after_upgrade: false
```

## Upgrading (and migrating) the database manually

It is also possible to manually upgrade the database. This can be useful if you want to, for example,
combine the database upgrade with a migration to a new server.

The steps are:
1. Deploy a new database server using Ansible. You can do this by adding the server that is to be the new
   database server to the database group in Ansible. Don't remove the current database server yet. If the
   environment is not yet on Yoda 1.9.x, you will have to set the database version explicitly in the `host_vars`
   of the new database server (not the `group_vars`), like so:

```yaml
enable_pgbouncer: true
postgresql_use_native_packages: false
pgsql_version: 15
```
   
   Ensure that locale settings for the old and new database server are identical, and that basic performance
   tuning has been configured (e.g. setting `effective_cache_size`).

2. Verify that locale of the old and new database are identical, using the `\l` command in `psql`.

3. Disable iRODS on the consumer (`sudo systemctl stop irods`), disable DavRODS and the portal on the portal/DavRODS/combi servers
   (`sudo systemctl stop httpd`) and disable iRODS on the provider (`sudo systemctl stop irods`).

4. Dump the present ICAT database on the old database server (you may want to do this in a tmux session on large environments). For example:

```
sudo -iu postgres pg_dump ICAT | gzip | sudo tee /var/dbbackup/icat-migration.sql.gz > /dev/null
```

5. Transfer the dump file to the new database server.

6. Load the dump file on the new database server:

```
sudo gunzip -c /var/dbbackup/icat-migration.sql.gz | sudo -iu postgres psql ICAT
```

7. Disable the old database:

```
sudo systemctl stop postgresql
sudo systemctl disable postgresql
```

8. Move the new database configuration to the `group_vars`, and remove the old database server from the database group. It is
   generally also recommended to enable Yoda-specific database indexes at this point (`irods_database_enable_yoda_indexes: true`),
   unless there is a specific reason not to use them on the environment. Adjust `irods_database_fqdn` to point to the new
   database server.

9. Adjust the `/etc/irods/server_config.json` Postgres database plugin configuration by setting `db_host` and `db_port` to the values
   for the new database server. The port is typically 6432 if PgBouncer is enabled, otherwise 5432.

10. Restart iRODS.

11. Run the Ansible playbook. You should now have an environment where the new database server has been deployed, iRODS should now talk
    to the new database server. Verify that basic functionality of iRODS works (e.g. by examining the output of the `ils` command) and
    check that iRODS is talking to the new database server (e.g. by viewing the number of transactions in the pgbouncer log file on the
    new database server). Disregard any PostgreSQL warning messages in the logs at this step.

12. Check the database plugin configuration in the `/etc/irods/server_config.json` configuration file. Ensure that `db_odbc_driver` is
    set to `"PostgreSQL"`. If the database plugin still has a `db_odbc_type` parameter, remove it. Restart iRODS if any manual changes
    were needed in this step.

13. Verify that Yoda works as expected.

14. Remember to update database backup and monitoring scripts so that they point to the new database.
