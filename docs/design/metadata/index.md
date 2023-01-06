---
title: Metadata
parent: Software Design
nav_order: 2
has_children: true
---
# Metadata

## Overview

Yoda supports adding metadata to collections. This facilitates archiving and (especially) publishing
a collection of data as a data package. Each community or group can have its own metadata schema,
so that different departments or faculties can optionally adapt the metadata format to their field.

This part of the documentation is about metadata in the context of Yoda data packages. iRODS metadata (AVUs)
have a role in Yoda metadata, but can also be used for other purposes that are unrelated to Yoda data
packages. Data request module metadata is also not in the scope of this page.

Yoda metadata is primarily stored in data objects named `yoda-metadata.json`.

## Metadata schemas

In Yoda, a metadata schema is used to validate the metadata of a data package. The schema also
contains information regarding how the metadata should be displayed in the web portal.

A Yoda metadata schema contains of two parts:

1. A JSON schema file that is used to validate metadata of a data package.
2. A UI schema file that contains information for the web portal regarding how to display a metadata
   form for this schema, optionally including placeholders and help text for each field.

Yoda environments have a default metadata schema. Additionally, specific metadata schemas can be
configured for communities (also known as categories). As of Yoda 1.9, it is also possible to configure
a metadata schema on a group level.

For more information, see:
* [Metadata schema configuration](schema-configuration.md)
* [Using JSON schema to define a metadata schema](metadata-form-json.md)

## Schema names and identifiers

Each schema has a globally unique identifier (URL) that is based on its name. For example, the *default-2
schema* is identified as `https://yoda.uu.nl/schemas/default-2/metadata.json`.

For more information, see [ADR schema identifiers](adr-schema-identifiers.md)

## Exporting of metadata during publication

When a data package is published, its metadata will be exported in three ways:

### Landing page

The landing page HTML code is generated using a Jinja2 template. This template may need to be adapted
in case of metadata schema changes. The template can be found in
`/etc/irods/yoda-ruleset/templates/landingpage.html.j2`. The Ansible playbook activates this template
by uploading it to the `/zone/yoda/templates/` collection.

### JSON file for DataCite

A JSON file conforming to the DataCite v4 Schema is generated. The implementation can
be found in `/etc/irods/yoda-ruleset/json_datacite41.py`.

### OAI-PMH data

The metadata will be copied to the OAI-PMH server (public server). Once there, it will
be processed by [MOAI](../../design/overview/yoda-moai.md) so that it can be harvested
using the [OAI-PMH protocol](https://en.wikipedia.org/wiki/Open_Archives_Initiative_Protocol_for_Metadata_Harvesting)
by external systems.  Only a subset of fields that map to Dublin core and DataCite are processed by MOAI.
Any changes to these fields will result in the metadata being omitted from the stream.

# Metadata transformation

As a general rule, metadata will have to comply with the latest version of a schema. For example,
if a new version of Yoda has a new `default-2` schema, all data packages using the `default-1` schema
will need to be updated to `default-2`..

Vault metadata is upgraded as a part of the upgrade process, as described in the release notes. Research
metadata is updated when a user opens it.

The transformation logic for updating to a newer version of a schema is defined in
`/etc/irods/yoda-ruleset/schema_transformations.py`.

## Further information

* [Information about metadata form implementation](metadata-form.md)
* [Use of metadata in the vault](metadata-vault.md)
