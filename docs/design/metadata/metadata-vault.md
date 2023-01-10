---
title: Metadata vault
grand_parent: Software Design
parent: Metadata
---
# Metadata of data packages in the vault

## Submit to vault

When a user submits a data package to the vault, its metadata will be validated first against
the metadata schema.

## Editing metadata in vault

The metadata form is also used for editing of metadata when the data package has already been accepted and copied to the vault.
A **data manager**, a Yoda user that is member of a datamanager group for the same research group, can still edit metadata of
a package in the vault.

## Metadata form for the vault

The vault metadata form uses the same JSON schema as the research group.  Therefore, the form layout and validation are identical
to the research group metadata form.

## Metadata versioning in the vault

In contrast to metadata in research groups, metadata in vault groups is versioned. That is, the original metadata
when the data package was submitted is kept in the `yoda-metadata.json` file in the `original` collection of the data
package. Metadata versions starting from the time the data package was submitted to the vault have a numeric suffix
that indicates the version. This number can also be used to order the metadata version by date and time, so that Yoda
can determine which version is the latest. 

Examples of metadata file names:

```
yoda-metadata[1554743001].json
yoda-metadata[1554733000].json
```
