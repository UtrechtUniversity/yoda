---
grand_parent: Software Design
parent: Metadata
---
# ADR Metadata schema identifiers

## Introduction

This document describes how the Yoda metadata schema identifier format was decided on.

## Principles

* Referable: the URI needs to be referenced from metadata files. It should be easy to reference for human and machine readers: URI syntax, not too long, minimal characters that require encoding. The schemas will be public, so no authentication/authorization.

* Scalable: The number of schemas will increase for different communities within and potentially outside UU, and there may be multiple schemas within a community, and there may be alternative serializations of a schema. We must ensure that each of these can be identified/referenced.

* Identifiable: Each schema should be identified uniquely. Each identifier may not be reused for another schema, version and/or community. We will reserve latest and current as versions.

* Durable: The references to the schemas may last for a long time. The solution must be able to survive most changes of the system and organizations so that these references remain valid. Thus a durable protocol (http), hostname (simple/governance) and path (easy to redirect via webserver)

* Maintainable: Easy to maintain structure and files via e.g. Git, and to add new schemas or versions.

* Automatable: The schemas will be retrieved mainly by software/machines. Identifier structure and location/retrieval-functions should comply with standards. We avoid the use of complex characters that will need encoding.

## Accepted proposal for identifier format

The format is `https://yoda.uu.nl/schemas/<schemaName>-<schemaVersion>/<schemaFile>`

* `https://` - protocol

* `yoda.uu.nl` – hostname

* `/schemas` – exclusive path reserved for schemas, to avoid conflicts with other resources on that the host. Implies that no other software on this host may use this path.

* `<schemaName>` - can be anything, but must be unique for all schemas published at yoda.uu.nl.

* `<schemaVersion>` - there can be multiple versions of a schema, which may be consecutive, but do not need to be. A schemaVersion must be unique per schemaName. We reserve latest and current as schemaVersions (this may be used as a symlink to the latest or current version in the future).

* `<schemaFile>` - metadata.json / uischema.json

## FAQs and considered alternatives

* Why https? https can be addressed from iRODS environments.

* Why yoda.uu.nl? We don’t want to depend on the current instances (i-lab, youth, ..) and don’t have sufficient authority on uu.nl. We don’t prefer data.uu.nl, as this may be addressed via other protocols than https, such as iRods.

* Why no community in path? There are non-community schemas such as datacite and schemas shared among communities. One may refer to a community in the schemaName.

* Why schemas and not meta? We assume that vocabularies or ‘non-informational URIs’ will be provided/published by another facility. Currently all published resources are related to a schema (definitions, transformations).

* Why not use persistent identifiers? This provides complexity in maintenance and retrieval. We believe that a well-chosen URI scheme can address most issues that a PID addresses.

* How to support research- and vault schemas? We may consider these to be different schemas, or different versions, or different representations of the same version. We consider the distinction between these as a work-around, hence we consider these to be different representations.

* How to ensure uniqueness? This is ensured hierarchically. As we share the hostname and schema-path, only the schemaName, schemaVersion and combination of those should be governed. We propose to make Yoda administration responsible for the unique schemaNames, and the schemaVersions. To avoid mixup of names and versions, we prohibit the use of the separator (hyphen, “-“) within the schemaName and the schemaVersion. To avoid conflicts of typical schemaNames among communities, we recommend to prefix these with the community name.

* How to determine equality? See RFC on URI syntax (this ignores e.g. portnumbers and authentication aspects in the URI, and considers the schema and hostname to be case insensitive). We recommend to treat schemaName, schemaVersion and schemaFile as case insensitive.

## Examples of schema identifiers that use this format

* [default-1 metadata.json](https://yoda.uu.nl/schemas/default-1/metadata.json)
* [default-1 uischema.json](https://yoda.uu.nl/schemas/default-0/uischema.json)
