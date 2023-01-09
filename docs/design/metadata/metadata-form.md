---
grand_parent: Software Design
parent: Metadata
---
# Metadata form implementation

This page contains implementation information about the metadata form functionality.

## Form functionality

The metadata form can be used in two ways. Firstly, regular users can use the form
to view and edit the metadata of a data package. Secondly, the form can show data package
metadata in readonly mode, if metadata cannot be edited by the present user.

The form can be configured using metadata schemas (see [schema configuration](schema-configuration.md)
for details). Based on the configured schema, the form shows feedback to the user
regarding the completeness and validity of entered metadata. If the metadata is complete
and valid, the user can save it. In that case, it is stored in a user-editable `yoda-metadata.json`
file, and also copied to iRODS metadata (AVUs) of the collection. After a user has entered metadata,
the data package can optionally be submitted to the vault for archiving and/or publication.

## Integration of React form within Yoda

The directory `/research/metadata-form/src` in the Yoda-portal repository contains Yoda-specific JavaScript code
for the React form.
