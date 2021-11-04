---
title: Metadata schemas
grand_parent: Software Design
parent: Metadata
---
# Community dependent files for configuration of metadata handling

## Community dependency
Within Yoda, research is supported via groups;  administrative entities declaring which persons are allowed to participate in that particular research.

Each group within Yoda belongs to a community. A community (=category) can hold multiple groups.

Different communities may require community specific metadata to be added to their research datasets.
Yoda is designed in such a way that each community can have its own metadata definition.
It accommodates handling of community dependent metadata though configuration of the generic metadataform.

If such a community specific definition is not present the system will fall back unto the default definition each Yoda instance is always equipped with.

The metadata definition is declared in JSON schema’s.

A metadata configuration file should always include all information that is required to be able to publish the research datapackage, including its metadata.
The exact fields can be found in the `core-0` schema.


## Folder layout for category dependent schemas
Central folder for all configurational and statuent files related to metadata is:
`/zone/yoda/schemas`

Category (=community) dependency is dealt with by using subfolders like:
`/zone/yoda/schemas/ilab`

In this case ilab is the name of community "ilab".

Within the software presence of category configurations is always checked for first.  
If not available then the fallback is to the default configuration:

`/zone/yoda/schemas/default`

## Involved files and their purpose
Each folder will hold the following files:

### metadata.json
Configuration for the metadata form as used for a community.

### uischema.json
UI configuration for the metadata form as used for a community.
