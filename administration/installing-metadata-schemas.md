# Installing metadata schemas
For a fully functional research module, a metadata schema is required.
Currently we only have a default-0schema, default-1 schema and a core-0 schema.
These can be found in the irods-ruleset-uu in `schemas/`.
Below a description of the needed files per schema (using the default schema as example):

**metadata.json**
  A JSON file describing the metadata form.

**uischema.json**
  A JSON file describing how a given data type should be rendered as a form input component. It provides information on how the form should be rendered.

You can install this set with the `tools/install-metadata-schema.r` script. This script accepts five parameters:
resc, src, schema, category and update.


Parameter  | Default value                                   | Description
-----------|-------------------------------------------------|------------
resc	   | irodsResc	                                     | Name of default resource to put the files into
src        | /etc/irods/irods-ruleset-uu/schemas             | Source directory of files
schema     | default                                         | Schema to install
category   | default-1                                       | Install schema to all categories ('default-1') or install to a single category (category name)
update     | 0                                               | Update existing schema (1) or keep existing files (0)

In the default situation the default schema is installed in ``/${RODSZONE}/yoda/schemas/default``.

Example invocation to install (or update) schema 'default' for all categories:
```bash
irule -F install-metadata-schema.r '*resc="irodsResc"' '*src="/etc/irods/irods-ruleset-uu/schemas/"' '*schema="default-1"' '*category="default"' '*update=1'
```

Example invocation to install (or update) schema 'core-0' for category 'experimental':
```bash
irule -F install-metadata-schema.r '*resc="irodsResc"' '*src="/etc/irods/irods-ruleset-uu/schemas/"' '*schema="core-0"' '*category="experimental"' '*update=1'
```

If you want to install individual files without the script then you can use the iput command.
If you install the files in a directory with the same name as the name of a category it will become the schema for that category and that category alone, when the category is created afterwards. Existing categories without a specific schema will still use the default schema.
To update existing files use the force flag "-f".
See the example below. Please replace `${RODSZONE}` with the current iRODS Zone and `${CATEGORY}` with the category you want to install.

```bash
iput -f metadata.json /${RODSZONE}/yoda/schemas/${CATEGORY}/metadata.json
iput -f uischema.json /${RODSZONE}/yoda/schemas/${CATEGORY}/uischema.json
```

The above is legal bash if you define the `CATEGORY` and `RODSZONE` environment variables, for example:

```bash
export CATEGORY=default
export RODSZONE=tempZone
```

Mistakes are easily made as the commands are so similar, but different.
So please take care.
