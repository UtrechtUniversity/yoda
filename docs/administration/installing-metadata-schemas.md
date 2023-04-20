---
parent: Administration Tasks
title: Installing metadata schemas
nav_order: 6
---
# Installing metadata schemas
For a fully functional research module, a metadata schema is required.
All schemas can be found in the yoda-ruleset in `schemas/`.
Below a description of the needed files per schema (using the default schema as example):

**metadata.json**
  A JSON file describing the metadata form.

**uischema.json**
  A JSON file describing how a given data type should be rendered as a form input component. It provides information on how the form should be rendered.

In the default situation the default schema is installed in ``/${RODSZONE}/yoda/schemas/default``.

Example to install (or update) schema 'default-2' as default for all categories:
```bash
irsync -Krv -R irodsResc /etc/irods/yoda-ruleset/schemas/default-2/ i:/${RODSZONE}/yoda/schemas/default/
```

## Yoda v1.8 and older
If you install the files in a directory with the same name as the name of a category it will become the schema for that category and that category alone, when the category is created afterwards. Existing categories without a specific schema will still use the default schema.

Example to install (or update) schema 'core-1' for category 'experimental':
```bash
irsync -Krv -R irodsResc /etc/irods/yoda-ruleset/schemas/core-1/ i:/${RODSZONE}/yoda/schemas/experimental/
```

The above is legal bash if you define `RODSZONE` environment variable, for example:

```bash
export RODSZONE=tempZone
```

Mistakes are easily made as the commands are so similar, but different.
So please take care.

## Yoda v1.9 and later
From Yoda v1.9 and later it is possible to set metadata schemas on group level.
For this a schema needs to be installed and marked selectable.

Example to install (or update) schema 'core-1':
```bash
irsync -Krv -R irodsResc /etc/irods/yoda-ruleset/schemas/core-1/ i:/${RODSZONE}/yoda/schemas/core-1/
```

Ensure the schema is selectable when creating a group in the group manager:
```bash
imeta set -C /${RODSZONE}/yoda/schemas/core-1 org_schema_user_selectable True
```

The above is legal bash if you define `RODSZONE` environment variable, for example:
```bash
export RODSZONE=tempZone
```
