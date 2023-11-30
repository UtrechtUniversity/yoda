---
parent: Administration Tasks
title: Troubleshooting replication and revision creation
nav_order: 12
---
# Troubleshooting replication and revision creation

Revision creation and replication of data objects are handled asynchronously. Policies
add metadata attributes to data objects that need to be replicated or have a new revision.
The replication and revision creation cronjobs process these data objects asynchronously.

Generic information about these background jobs can be found on
[the page about background processes](../design/processes/asynchronous-processes.md). This page
contains advice regarding how to troubleshoot these processes.

In Yoda 1.9 and higher, the revision and replication jobs run in verbose mode by default, which means
the rodsLog typically has information regarding which data objects are being processed by these
jobs. A good first step is to look up in the rodsLog what the relevant job is doing and
whether the jobs show any errors, in particular permission errors (which are a common cause of
replication/revision errors). When in doubt about whether permissions are correct, you can use
the `iget` command to verify that a data object is accessible to the rods account.

If a job is not configured to run in verbose mode, you can run it in verbose mode manually
(see below).

## Running a job in verbose mode manually

If a data object is not replicated or does not get a new revision, first check whether this behaviour
is caused by configured delay parameters (`async_replication_delay_time` and ` async_revision_delay_time`).
If this is not the case, consider stopping and temporarily disabling the background process cronjob for
troubleshooting. This can be done by temporarily setting the background process stop flag
(`/ZONE/yoda/flags/stop_replication` or `/ZONE/yoda/flags/stop_revisions`) and waiting for the job to
finish. See [the page about setting job flags](setting-job-flags.md) for more information.

The iquest command can be used to print a list of data objects that are queued for replication
or revision creation.  Example for replication:

```
iquest "%s/%s" --no-page "SELECT COLL_NAME, DATA_NAME  where META_DATA_ATTR_NAME = 'org_replication_scheduled'"
```

If it seems that the background job is failing, or a data object is not getting processed despite having
the expected metadata attribute, you could run the background job in verbose mode. Remember to remove the
stop flag of the process first; otherwise the background job will not start.  If many data objects (or large data objects)
are queued for replication or revision creation it may be advisable to run the job in a tmux session. Running the jobs
in verbose mode will log additional information about data objects being processed to the rodsLog. Example
command for the replication job:

```
/bin/python /etc/irods/yoda-ruleset/tools/async-data-replicate.py -v
```

## Running a job in dry run mode

Both the replication and revision creation jobs can be run in dry run mode, which means that they will not create any replications or revisions, but simulate what would happen if they did. The parameters are `async_replication_dry_run` and ` async_revision_dry_run` for replication and revision, respectively.