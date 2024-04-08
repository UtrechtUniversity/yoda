---
parent: Administration Tasks
title: Troubleshooting data package archival in the vault
nav_order: 16
---
# Troubleshooting data package archival in the vault

After a data manager approves a data package for archiving in the vault, the
`retry-copy-to-vault.r` cronjob asynchronously archives the data package.
This involves copying its data from the research collection to the vault
collection, among other things. By default, this process happens automatically.
Please consult [the vault process design documentation](../design/processes/vault-process.md)
for more details.

This page contains an explanation of how to troubleshoot the process if something
goes wrong.

## Detecting failed archiving jobs

Archival jobs that have failed can be detected using the
[data package status report tool](https://github.com/UtrechtUniversity/yoda-clienttools?tab=readme-ov-file#yreport_datapackagestatus),
which is part of the [Yoda client tools](https://github.com/UtrechtUniversity/yoda-clienttools).

You can also run this tool in a cronjob to send a report of data packages that
are in the process of being archived or published for a long time, which suggests
that something might have gone wrong.

Example command for compiling a list of data packages that have been in the process
of being archived or published for more than approximately four hours, and sending
the list to an administrator if there are any:

```
yreport_datapackagestatus --pending --stale --email a.admin@uu.nl
```

This will also report data packages that are waiting for approval to be archived
or published. In such cases, no technical troubleshooting is needed.

## Finding the cause

If the data package has been approved for archiving in the vault (status `ACCEPTED`),
first see if the cause of the problem can be found in the rodsLog files. Find the
`iiCopyFolderToVault` message for the data package in the rodsLog. Then grep for other
messages by the same pid on the same day, and look for error messages.

Possible causes include:
- An issue with one of the source data objects in the research collection results in a failure
  when copying it. For example: a data object that is in an intermediate state cannot be copied.
- A restart of the iRODS service while the copy-to-vault process was running.
- A storage issue, such as a storage resource without free space available.

If the root cause is not transient, it needs to be resolved first. Otherwise restarting
the process would just result in the same problem occurring again.

## Restart options

There are two ways to restart the transfer:

### Trigger a complete restart of the copy-to-vault process for the data package

Signal the copy-to-vault job to retry the archiving operation by setting the
`org_cronjob_copy_to_vault` AVU to `CRONJOB_RETRY`. The job will then copy the
data packages to a new vault folder.

Example command:

```
imeta set -C /tempZone/home/vault-collection/data-package[1234567890] org_cronjob_copy_to_vault CRONJOB_RETRY
```

Afterwards, you will need to remove the vault collection that was created on the first try manually.

### Finish the archiving process manually

If the error occurred during copying the contents of the data packages, it is also possible to finish
the copy job manually. This can be useful if the data package is large and retrying the complete transfer
would take a lot of time.

First, complete the synchronization process using the `irsync` command in a `tmux` session. For example:

```
irsync -r -V -s "i:/zoneName/home/research-groupname/data-package" "i:/zoneName/home/vault-groupname/data-package[1234567890]/original"
```

After `irsync` has finished, complete the copy-to-vault process manually using the `secure-in-vault` rule. Example command:

```
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/secure-in-vault.r '*researchCollection="'""/zoneName/home/research-groupname/data-package'"' '*vaultCollection="'"/zoneName/home/vault-groupname/data-package[1234567890]"'"'
```

Finally, check in the portal that the status of the data package in the research collection is `Secured`,
the publication status is `Unpublished`, and the metadata of the vault package can be viewed. Also check the
rodsLog for errors.
