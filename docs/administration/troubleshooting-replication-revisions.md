# Troubleshooting replication and revision creation

Revision creation and replication of data objects are handled asynchronously. Policies
add metadata attributes to data objects that need to be replicated or have a new revision.
The replication and revision creation cronjobs process these data objects asynchronously.

Generic information about these background jobs can be found on
[the page about background processes](../design/processes/asynchronous-processes.md). This page
contains advice regarding how to troubleshoot these processes.

If a data object is not replicated or does not get a new revision, consider first stopping and
temporarily disabling the background process cronjob for troubleshooting. This can be done
by temporarily setting the background process stop flag (`/ZONE/yoda/flags/stop_replication` or
`/ZONE/yoda/flags/stop_revisions`) and waiting for the job to finish.

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
/bin/python /etc/irods/irods-ruleset-uu/tools/async-data-replicate.py -v
```

Failures during revision creation are often caused by permission problems. First run the cron job in
verbose mode to determine which data object is causing the problem. Then verify that the data object
is accessible to the rods account, e.g. using an `iget` command.
