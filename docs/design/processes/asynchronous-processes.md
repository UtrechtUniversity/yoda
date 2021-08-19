---
grand_parent: Software Design
parent: Processes
---
# Asynchronous processes

This page contains an overview of asynchronous processes in Yoda.

## Table of contents

* [Metadata](#metadata)
* [Metadata schema update job](#metadata-schema-update-job)
* [Replication](#replication)
* [Replication job](#replication-job)
* [Revision management](#revision-management)
* [Revision management - creation job](#revision-creation-job)
* [Revision management - cleanup job](#revision-cleanup-job)
* [Statistics](#statistics)
* [Statistics job](#statistics-job)
* [Archiving](#archiving)
* [Archiving - retry-copy-to-vault job](#archiving-retry-copy-job)
* [Archiving - intake to vault job](#archiving-intake-to-vault-job)
* [Archiving - publication job](#archiving-publication-job)
* [Archiving - vault integrity job](#archiving-vault-integrity-job)

<a name="metadata"/>

## Metadata

Metadata changes are handled synchronously, except for batch updates of data package metadata
after schema updates.

<a name="metadata-schema-update-job"/>

### Schema update job

|   |   |
|---|---|
| Script               | /etc/irods/irods-ruleset-uu/tools/check-metadata-for-schema-updates.r       |
| Purpose              | verify and update data package metadata to new schema versions              |
| Lock file            | no locking                                                                  |
| Scheduling           | delayed rule queue                                                          |
| Typically started by | manually by application administrator, after schema or application upgrade  |

Any changes to data package metadata will be recorded in the rodsLog.

<a name="replication"/>

## Replication

By default, data in Yoda is replicated across two servers. Policies add a metadata attribute
to data objects that should be replicated, and the asynchronous replication job replicates these
objects. The default name of the metadata attribute is `org_replication_scheduled`; the attribute value
contains the source and destination resource, separated by commas.

<a name="replication-job"/>

### Replication job

|   |   |
|---|---|
| Script               | /etc/irods/irods-ruleset-uu/tools/async-data-replicate.py                   |
| Purpose              | replicate data objects to consumer                                          |
| Lock file            | /tmp/irods-async-data-replicate.py.lock                                     |
| Scheduling           | cronjob, data object queue based on data object metadata attributes         |
| Typically started by | cronjob runs every five minutes                                             |

Data objects are marked for revision creation using a metadata attribute. The default name of these
attributes is `org_replication_scheduled`.

The script has a verbose mode (which can be enabled using the `-v` switch). This will log additional
information for troubleshooting to the rodsLog.

If a flag data object named `/ZONE/yoda/flags/stop_replication` is present, the script will stop
processing data objects.

<a name="revision-management"/>

## Revision management

Yoda supports revision management of data objects, so that users can recover older versions of files.
Old revisions are removed regularly using a [revision strategy](revisions.md). Both revision creation
and revision cleanup are handled asynchronously.

<a name="revision-creation-job"/>

### Revision creation job

|   |   |
|---|---|
| Script               | /etc/irods/irods-ruleset-uu/tools/async-data-revision.py                    |
| Purpose              | create revisions of data objects                                            |
| Lock file            | /tmp/irods-async-data-revision.py.lock                                      |
| Scheduling           | cronjob, queue based on data object metadata attributes                     |
| Typically started by | cronjob runs every five minutes                                             |

Data objects are marked for revision creation using a metadata attribute. The default name of these
attributes is `org_revision_scheduled`.

The script has a verbose mode (which can be enabled using the `-v` switch). This will log additional
information for troubleshooting to the rodsLog.

If a flag data object named `/ZONE/yoda/flags/stop_revisions` is present, the script will stop
processing data objects.

<a name="revision-cleanup-job"/>

### Revision cleanup job

|   |   |
|---|---|
| Script               | /var/lib/irods/.irods/cronjob-revision-cleanup.sh                           |
| Purpose              | remove unneeded revisions of data objects, as per revision strategy         |
| Lock file            | no lock file                                                                |
| Typically started by | daily cronjob                                                               |

<a name="statistics"/>

## Statistics

The statistics module provides users with an overview of the amount of data stored in Yoda groups
and communities.

<a name="statistics-job"/>

### Statistics job

|   |   |
|---|---|
| Script               | /etc/irods/irods-ruleset-uu/tools/monthly-storage-statistics.r              |
| Purpose              | record size of data in group metadata                                       |
| Lock file            | no lock file                                                                |
| Typically started by | monthly cronjob                                                             |

<a name="archiving"/>

## Archiving and publication

Asynchronous jobs are also used to copy data packages from a research or intake folder to the vault,
as well as to process publications. Furthermore, an asynchronous job for verifying vault data integrity
is available.

<a name="archiving-retry-copy-job"/>

### Retry copy to vault job

|   |   |
|---|---|
| Script               | /etc/irods/irods-ruleset-uu/tools/retry-copy-to-vault.r                     |
| Purpose              | copy data packages from research groups to the vault                        |
| Lock file            | no lock file, but collection metadata attribute records processing status   |
| Typically started by | cronjob, runs every minute                                                  |

By default, groups that are to be copied to the vault are marked with a metadata attribute named
`cronjob_copy_to_vault`.

<a name="archiving-intake-to-vault-job"/>

### Intake copy to vault job

|   |   |
|---|---|
| Script               | /var/lib/irods/.irods/job_movetovault.r                                     |
| Purpose              | copy data packages from intake groups to the vault                          |
| Lock file            | uses lock attribute on the vault folder                                     |
| Typically started by | cronjob, runs every five minutes                                            |

<a name="archiving-publication-job"/>

### Process publication job

|   |   |
|---|---|
| Script               | /etc/irods/irods-ruleset-uu/tools/process-publication.r                     |
| Purpose              | Asynchronously handles publication and depublication of data packages       |
| Lock file            | no lock file, but status is recorded in metadata                            |
| Typically started by | cronjob, runs every minute                                                  |

<a name="archiving-vault-integrity-job"/>

### Vault integrity check job

|   |   |
|---|---|
| Script               | irods-ruleset-uu/tools/check-vault-integrity.r                              |
| Purpose              | Verifies checksums of data objects in the vault                             |
| Scheduling           | Delayed rule queue                                                          |
| Typically started by | manually by administrator                                                   |

All data objects with data integrity issues are logged in the rodsLog. Verifying vault integrity
can take a long time. The batch script adds 256 jobs per 60 seconds to the rule queue in order to
manage the load on the server.
