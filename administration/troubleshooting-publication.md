# How to deal with hanging publications

When a publication stays in Approved status for an extended period of time (longer than cronjob interval) something probably went
wrong. Here are some troubleshooting hints.

First look for `iiProcessPublication` in `/var/lib/irods/log/rodsLog`. It will show the processing of the publication.

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

When the problem is caused by invalid metadata, check the value of `org_publication_combiXmlPath` and `org_publication_dataCiteXmlPath`. You can use iget to download the generated metadata at these paths and check for XML/XSLT related problems.


When the `org_publication_status` is `Retry` the publication process will be retried until success.
Check status.datacite.org if you suspect a DataCite problem.
Publications will fail if the API servers are down.  
Check the ability of the rods user to set up a ssh connection with the inbox user on the public Yoda server.
When troubleshooting was successful the publication process will skip the subtasks
before the failure and continue.

When the `org_publication_status` is `Processing` and the root cause of the crash looks to be incidental, you could set the status to `Retry` with  imeta on the `org_publication_status`. The publication will be retried the next time the cronjob runs.

```bash
imeta set -C /tempZone/home/vault-test/research-test[123456789] org_publication_status Retry
```


When the `org_publication_status` is `Unrecoverable` then one of XSLT conversion steps have produced invalid metadata.
You could use a third party XSLT processor on the metadata in the previously mentioned source XML files with the used XSL's from the current category.
This could tell you the problem.
If the metadata generation succeeds but is still invalid according to the DataCite API, you could use an XSD validator on the datacite.xml using the version 4 XSD's found at schema.datacite.org.
