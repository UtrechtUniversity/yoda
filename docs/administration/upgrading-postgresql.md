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

Yoda versions 2.0 and onwards work with PostgreSQL 15 by default. Starting from Yoda 2.1, it is possible to upgrade to PostgreSQL 18.

## Upgrade methods

Existing Yoda environments can be upgraded to PostgreSQL 18 by either starting the upgrade from Ansible, or by dumping and restoring the database
manually onto a new upgraded server.

Regardless of which method you choose, the following advice applies:
- Ensure that you have a recent database backup before starting the upgrade process.
- First perform the upgrade process on an (acceptance) test environment that resembles your production environments. This also helps with estimating
how much time and diskspace you will need for upgrading the production environment.
- A database upgrade is a good opportunity to review the Yoda [configuration parameters](configuring-yoda.md) for PostgreSQL, and to see if any
improvements can be made in areas such as performance tuning.

## Upgrading the database on the same server: upgrade with Ansible

The Ansible playbook contains an option for upgrading the database automatically. Please note: upgrading the database may take a significant time on
large environments.

For Yoda 2.1.x and later, use the following configuration parameters:
   ```yaml
   pgsql_version: 18

   postgresql_perform_db_upgrade: true
   postgresql_remove_old_data_after_upgrade: false
   ```

## Upgrading (and migrating) the database on a new server: upgrade manually

If you want to combine the database upgrade with a migration to a new server, it is possible to upgrade the database manually.

The steps are:
1. Deploy a new database server using Ansible. You can do this by adding the server that is to be the new
   database server to the database group in your `hosts` file in Ansible. Do not remove the current database server yet. If the
   environment is not on Yoda 2.1.x yet, you will have to set the database version explicitly in the `host_vars`
   of the new database server (not the `group_vars`), like so:

   ```yaml
   enable_pgbouncer: true
   pgsql_version: 18
   ```

   Ensure that locale settings for the old and new database server are identical, and that basic performance
   tuning has been configured (e.g. setting `effective_cache_size`).

2. Verify that locale of the old and new database are identical, using the `\l` command in `psql`.

3. Stop iRODS on the consumer (`sudo systemctl stop irods`), stop DavRODS and the portal on the portal/DavRODS/combi servers
   (`sudo systemctl stop apache2` for Debian, `sudo systemctl stop httpd` for RedHat), and stop iRODS on the provider (`sudo systemctl stop irods`).

4. Dump the present ICAT database on the old database server (you may want to do this in a tmux session on large environments). For example:
   ```
   sudo -iu postgres pg_dump ICAT | gzip | sudo tee /var/dbbackup/icat-migration.sql.gz > /dev/null
   ```

5. Transfer the dump file to the new database server.

6. Load the dump file on the new database server:
   ```
   sudo gunzip -c /var/dbbackup/icat-migration.sql.gz | sudo -iu postgres psql ICAT
   ```

7. If the old database is no longer in use by anything else, it can be disabled: 
   ```
   sudo systemctl stop postgresql
   sudo systemctl disable postgresql
   ``` 
   If it is still in use (for example, as an EUS database), then it can be upgraded separately.

8. If the old database server needs to be upgraded as well, move the new database configuration to the `group_vars`. Otherwise, leave it in the `host_vars`. 

9. Adjust `irods_database_fqdn` in the `group_vars` to point to the new database server. It is generally also recommended to enable Yoda-specific database
   indexes at this point (`irods_database_enable_yoda_indexes: true`), unless there is a specific reason not to use them on the environment.

10. Remove the old database server from the database group in the `hosts` file. 
   
11. On the provider, adjust the `/etc/irods/server_config.json` database plugin configuration by setting `host` and `port` to the new database
   server values. The port is typically 6432 if PgBouncer is enabled, otherwise 5432. If the database plugin configuration still has Postgres
   values `db_host` and `db_post`, you can remove them as they are outdated.

12. As iRODS user, ensure the ODBC connection details (`~/.odbc.ini`) point to the new database server.

13. Restart iRODS on all servers, then ensure PgBouncer is connecting properly (you can do so by checking the PgBouncer log).

14. Run the Ansible playbook. You should now have an environment where the new database server has been deployed, iRODS should now talk
    to the new database server. Verify that basic functionality of iRODS works (e.g. by examining the output of the `ils` command) and
    check that iRODS is talking to the new database server (e.g. by viewing the number of transactions in the PgBouncer log file on the
    new database server). Disregard any PostgreSQL warning messages in the logs at this step.

15. Check the database plugin configuration in the `/etc/irods/server_config.json` configuration file and ensure that `odbc_driver` is
    set to `"PostgreSQL"`. If the database plugin configuration still has a `db_odbc_driver` or a `db_odbc_type` parameter, you can remove 
    them as they are outdated. Restart iRODS if any manual changes were needed in this step.

16. Verify that Yoda works as expected.

17. Remember to update database backup and monitoring scripts so that they point to the new database.

## Cleanup after upgrade

If you wish to clean up the data of the old PostgreSQL version after the upgrade, you can use the following configuration parameter and then
re-run the Ansible playbook:
   ```yaml
   postgresql_remove_old_data_after_upgrade: true
   ```