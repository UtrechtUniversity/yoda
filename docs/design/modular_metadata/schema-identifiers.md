---
grand_parent: Software Design
parent: Modular metadata
---
# Modular metadata schema identifier format

## Introduction

This document describes the Yoda modular metadata schema identifier format.

## Principles

- Referable: the URI needs to be referenced from metadata files. It should be easy to reference for human and machine readers: URI syntax, not too long, minimal characters that require encoding. The schemas will be public, so no authentication/authorization.

- Scalable: The number of schemas will increase for different communities within and potentially outside UU, and there may be multiple schemas within a community, and there may be alternative serializations of a schema. We must ensure that each of these can be identified/referenced.

- Identifiable: Each schema should be identified uniquely. Each identifier may not be reused for another schema, version and/or community. We will reserve latest and current as versions.

- Durable: The references to the schemas may last for a long time. The solution must be able to survive most changes of the system and organizations so that these references remain valid. Thus a durable protocol (https), hostname (simple/governance) and path (easy to redirect via webserver)

- Maintainable: Easy to maintain structure and files via e.g. Git, and to add new schemas or versions.

- Automatable: The schemas will be retrieved mainly by software/machines. Identifier structure and location/retrieval-functions should comply with standards. We avoid the use of complex characters that will need encoding.

## Identifier format
The format is `https://<metadataRepo>/schemas/<schemaName>_<schemaVersion>/<schemaFile>`

- `https://` protocol
- `<metadataRepo>` metadata repository FQDN
- `/schemas` exclusive path reserved for schemas, to avoid conflicts with other resources on the host. Implies that no other software on this host may use this path.
- `<schemaName>` schema name
- `<schemaVersion>` schema version
- `<schemaFile>` schema file (metadata.json or uischema.json)

## Requirements & constraints

### Schema name (schemaName)
- Must be unique across all schemas within a Yoda instance
- Must contain alphabetic characters only (a–z) and hyphens (not as first character); no digits, underscores (schemaVersion separator), dots, colons, or special characters permitted
- Schema names are case-insensitive; recommend lowercase in practice
- Recommended to prefix with community name (e.g., `cellbiology-keywords`) to avoid naming conflicts across communities
- Should be concise and human-readable

### Schema version (schemaVersion)
- Must be unique per schemaName; no two versions of the same schema may share an identifier
- Must follow MODEL-REVISION-ADDITION format (e.g., `1-0-5`, `2-3-1`) according to SchemaVer semantics:

    When versioning a data schema, we are concerned with the backwards-compatibility between the new schema and existing data represented in earlier versions of the schema.
    This is the fundamental building block of SchemaVer, and explains the divergence from SemVer.

    Given a version number MODEL-REVISION-ADDITION, increment the:

    * MODEL when you make a breaking schema change which will prevent interaction with any historical data
    * REVISION when you make a schema change which may prevent interaction with some historical data
    * ADDITION when you make a schema change that is compatible with all historical data

    Syntactically this feels similar to SemVer, but as you can see from the increment rules, the semantics of each element are different from SemVer.

### Schema file (schemaFile)
- Must be exactly one of the following:
  - `metadata.json` — schema definition
  - `uischema.json` — UI presentation schema
- Schema file names are case-insensitive; files should use lowercase in practice
- Other file types are not permitted in this identifier format; alternative schema representations require separate identifiers

### Metadata repository FQDN (metadataRepo)
- Must be a fully qualified domain name
- Should use a durable, simple hostname (e.g., `yoda.uu.nl` rather than `yoda-v2.old.uu.nl`)
- Must use https protocol (http not permitted)

## FAQs and considered alternatives

* Why https? https can be addressed from iRODS environments.

* Why no community in path? There are non-community schemas such as datacite and schemas shared among communities. One may refer to a community in the schemaName.

* Why schemas and not meta? We assume that vocabularies or ‘non-informational URIs’ will be provided/published by another facility. Currently all published resources are related to a schema (definitions, transformations).

* Why not use persistent identifiers? This provides complexity in maintenance and retrieval. We believe that a well-chosen URI scheme can address most issues that a PID addresses.

* How to support research- and vault schemas? We may consider these to be different schemas, or different versions, or different representations of the same version. We consider the distinction between these as a work-around, hence we consider these to be different representations.

* How to ensure uniqueness? This is ensured hierarchically. As we share the hostname and schema-path, only the schemaName, schemaVersion and combination of those should be governed. We propose to make Yoda administration responsible for the unique schemaNames, and the schemaVersions. To avoid ambiguity when parsing, we prohibit underscores within the schemaName and within the schemaVersion itself. Underscores separate schemaName from schemaVersion; hyphens separate components within schemaVersion (MODEL-REVISION-ADDITION). To avoid conflicts of typical schemaNames among communities, we recommend to prefix these with the community name.

* How to determine equality? See RFC on URI syntax (this ignores e.g. portnumbers and authentication aspects in the URI, and considers the schema and hostname to be case insensitive). We recommend to treat schemaName, schemaVersion and schemaFile as case insensitive.

## Examples of schema identifiers that use this format

* [citation_1-0-0 metadata.json]()
* [citation_1-0-0 uischema.json]()
