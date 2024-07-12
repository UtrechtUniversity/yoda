---
title: Metadata schemas
grand_parent: Software Design
parent: Metadata
---
# Yoda metadata schema configuration

This page describes how metadata schemas are stored in Yoda, and how Yoda
keeps track of what schema to use for each group.

## Schema storage

Schemas are stored in collection `/zone/yoda/schemas`, with each schema having
a separate subcollection.

## Internal structure of schemas

Each schema consists of two parts:

1. A JSON schema that is used to validate metadata of a data package (filename: `metadata.json`).
2. A UI schema file that contains information for the web portal regarding how to display a form
   for metadata with this schema, optionally including placeholders and help text for each field.
   This information is stored in files named `uischema.json`.

A minimal schema is available as the `core-1` schema.

## Schema configuration

### Research and deposit groups

In Yoda, metadata schemas of research and deposit groups can be defined on three levels:
1. On the environment level (the *default schema*)
2. On the community (also known as category) level
3. On the group level (in Yoda 1.9 and higher)

The most specific level has priority. That is: a group will use its configured schema. If it does
not have one, it will fall back to the community metadata schema. If the community has no configured
metadata schema, it will fall back to the default metadata schema.

The default schema and community-level schema need to be configured by a technical admin. They are
stored in a subcollection of `/zone/yoda/schemas/`. The default metadata schema is located in the
`default` subcollection, whereas the community-level schemas are stored in a subcollection with the
same name as the community. See [the page about installing metadata schemas](../../administration/installing-metadata-schemas.md)
for instructions about how to replace a schema.

Group level schemas are configured by the user who creates the group. The schema name is stored
in the `schema_id` AVU that is set on the research group.

### Vault groups

In Yoda 1.9.3 and lower, a vault group always has the metadata schema of its
research or deposit group.

In newer versions of Yoda, a technical admin can override the metadata schema of the vault group by
adding a `schema_id` AVU to the vault group itself. Furthermore, if a vault group has no matching research
group, no matching deposit group, and no `schema_id` AVU, it uses the environment default schema.
