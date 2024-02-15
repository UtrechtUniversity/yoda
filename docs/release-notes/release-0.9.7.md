---
parent: Release Notes
title: v0.9.7
nav_order: 99
---
# Release Notes v0.9.7

Version: 0.9.7

Released: August 2017

## What's new
### Features
- Folders in the research area can be secured in the vault
- A datamanager per category can approve packages for the vault and control
  read access within the vault
- File modifications can be reverted with the help of revisions
- Rules to restore a collection in mass
- Introduction of the statistics module
- Integration of the youth intake module

## Upgrading from previous release
Install the 0.9.7 version of at least yoda-ruleset and
irods-ruleset-research.

Install the latest version of implementation specific rulesets;
irods-ruleset-youth-cohort or irods-ruleset-i-lab for example

Run the following migration scripts as rodsadmin to enable new features:

*/etc/irods/yoda-ruleset/tools/createSystemCollections.r*
    This script creates system collections that are needed for metadata
    schema's and revisions. To enabe revisions run it as follows:

```bash
irule -F createSystemCollections.r "*enableRevisions=1"
```

*/etc/irods/yoda-ruleset/set-vault-permissions.r*
    This scripts makes the vault collections belonging to a research group
    visible and allows a datamanager to manage read-only access.

*/etc/irods/irods-ruleset-research/tools/migrate-locks.r*
    The locking mechanism and folder statuses have changed. This script will
    migrate these to the new situation.

*/etc/irods/irods-ruleset-research/tools/create-revision-stores.r*
    Existing research groups do not have a revision store. This script will
    create one and will create an initial revision for every data object found.
    This could be a long running process.

*/etc/irods/irods-ruleset-research/tools/install-default-xml-for-metadata.r*
    Only run this script when the default metadata schema hasn't been installed
    yet. If the main resource is not named "irodsResc" or if you don't want to
    use the "ilab" schema then adapt this call:

```bash
irule -F install-default-xml-for-metadata.r '*resc="irodsResc"' '*src="/etc/irods/irods-ruleset-research/tools/xml"' '*default="ilab"'
```

Update the portal by pulling in the 0.9.7 version of the yoda-portal,
yoda-portal-group-manager, yoda-portal-research, yoda-portal-statistics and if
applicable the youth intake portal module.

Copy the cronjobs cronjon-revision-cleanup.sh and
copy-accepted-folders-to-vault.r to /var/lib/irods/.irods and add them to the
crontab like the example below.


```crontab
0,5,10,15,20,25,30,35,40,45,50,55 * * *    * /bin/irule -F $HOME/.irods/job_movetovault.r >>$HOME/iRODS/server/log/job_movetovault.log 2> /dev/null
0 0 * *    * /bin/sh $HOME/.irods/cronjob-revision-cleanup.sh >> $HOME/iRODS/server/log/cronjob-revision-cleanup.log 2> /dev/null
*/2 * *    * *    /bin/irule -F $HOME/.irods/copy-accepted-folders-to-vault.r >> $HOME/iRODS/server/log/copy-accepted-folders-to-vault.log
```
To workaround a memory leak in the irodsReServer iRODS needs to be restarted
regularly. The restartifirodsisidle.sh script from the yoda-ruleset/tools
directory is meant to restart iRODS only if no jobs are running. It could be
included in a cronjob or invoked by monit using irodsReServer.monit also found
in the yoda-ruleset/tools directory.

## Known Issues

1. With the research ruleset loaded we see occasional glibc level errors in
   the logs. They have no noticeable impact on the user.

2. The iRODS server will get slower over time due to a memory leak. A
   workaround is suggested above in the upgrade section.

3. When storage data is available, different tiers are assigned, and all
   resources are then reset to the same tier, the statistics module may show a
   blank page.
