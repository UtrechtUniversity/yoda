---
parent: Administration Tasks
title: Troubleshooting publication
nav_order: 10
---
# How to deal with hanging publications

When a publication stays in Approved status for an extended period of time (longer than cronjob interval) something probably went
wrong. Here are some troubleshooting hints.

First look for `process_publication` (v1.8.5 or earlier) or `[publication]` (v1.9.0 or later) in `/var/lib/irods/log/rodsLog`.
It will show the processing of the publication.

- When a publication succeeds it will return status OK.
- When the publication process has caught an error, but has no recovery process it will return `Unrecoverable` as status.
- When the whole process was interrupted at a time the error could not be caught, the status will stay at `Processing`.
- When the publication process encountered a DOI collision it will set status to `Retry` and reset the generated random ID.
- When the publication process encounters connectivity problems with DataCite or the public server it will set the status to `Retry`.

Then look at the rodsLog around the time of the problem. Error messages could give you a hint on the root cause.

The publication process saves its state in metadata on the vault package. You can use imeta to list the details. See an example below.
```bash
imeta lsw -C /tempZone/home/vault-test/research-test[123456789] org_publication%
```

When the problem is caused by invalid metadata, check the value of `org_publication_combiJsonPath` and `org_publication_dataCiteJsonPath`.
You can use iget to download the generated metadata at these paths and check for JSON related problems.

When the `org_publication_status` is `Retry` the publication process will be retried until success.
Check status.datacite.org if you suspect a DataCite problem.
Publications will fail if the API servers are down.  
Check the ability of the rods user to set up a ssh connection with the inbox user on the public Yoda server.
When troubleshooting was successful the publication process will skip the subtasks before the failure and continue.

When the `org_publication_status` is `Processing` and the root cause of the crash looks to be incidental, you could set the status to `Retry` with  imeta on the `org_publication_status`. The publication will be retried the next time the cronjob runs.

```bash
imeta set -C /tempZone/home/vault-test/research-test[123456789] org_publication_status Retry
```

The publication rule can be set to verbose mode so that it logs additional information for troubleshooting
purposes. In order to enable this, set the `org_publication_verbose_mode` AVU on the system collection:

```bash
imeta set -C /tempZone/yoda org_publication_verbose_mode yes
```

After troubleshooting, verbose mode can be disabled by removing the `org_publication_verbose_mode` AVU.

When the `org_publication_status` is `Unrecoverable` then one of JSON conversion steps have produced invalid metadata.
You could use a third party JSON processor on the metadata in the previously mentioned source JSON files with the used JSON schemas from the current category / research group.
This could tell you the problem.
If the metadata generation succeeds but is still invalid according to the DataCite API, you could use an JSON validator on the DataCite JSON using the version 4 schemas found at schema.datacite.org.
