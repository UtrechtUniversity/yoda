# Installing Terms & Conditions
Terms and conditions for publication are also read from iRODS and presented to the user. It needs to be an HTML snippet
to be rendered correctly. A naming scheme is up to the administrator, the last .html file placed in
/rodsZone/yoda/terms will become the text presented to the user. In order for every user to be able to read the terms
a read ACL for public needs to be set.

```bash
iput -r /etc/irods/irods-ruleset-research/tools/terms /${RODSZONE}/yoda
ichmod -rM inherit  /${RODSZONE}/yoda/terms
ichmod -rM read public /${RODSZONE}/yoda/terms
```

To add a new terms file just put it in the yoda/terms collection with a new name, so the old terms are preserved.

```bash
iput "${TERMS}.txt" "/${RODSZONE}/yoda/terms/${TERMS}.txt"
```

Every vault package with an action log record "submitted for publication" before the create time of the new terms were
accepted under the old terms.
