# Installing metadata schemas, formelements and stylesheets
For a fully functional research module, a metadata schema is required.
Currently we only have a default schema (currently the same as the I-lab schema) and a test schema.
These can be found in the irods-ruleset-research in `tools/schemas/`.
Below a description of the needed files per schema (using the default schema as example):

**metadata.json**
  A JSON file describing the metadata form

**research.xsd**
  A schema describing the elements and their type of a yoda-metadata.xml

**vault.xsd**
  A schema describing the elements and their type of a yoda-metadata.xml with required fields

**avu.xsl**
  A stylesheet to convert a yoda-metadata.xml to a AVU XML that can be loaded into iRODS with msiLoadMetadataFromXML(Buf)

**datacite.xsl**
  A stylesheet to convert a combi.xml consisting of user metadata from a yoda-metadata.xml file and system metadata into
  the DataCite XML format

**landingpage.xsl**
  A stylesheet to convert a combi.xml into a landingpage html file

Below a description of the other needed files:

**schema-for-xsd.xsd**
  A schema to validate XSD schema's.

**emptylandingpage.xsl**
  A stylesheet to convert a combi.xml into a empty landingpage html file

You can install this set with the `tools/install-metadata-schema.r` script. This script accepts five parameters:
resc, src, schema, category and update.


Parameter  | Default value                                   | Description
-----------|-------------------------------------------------|------------
resc	   | irodsResc	                                     | Name of default resource to put the files into
src        | /etc/irods/irods-ruleset-research/tools/schemas | Source directory of files
schema     | default                                         | Schema to install
category   | default                                         | Install schema to all categories ('default') or install to a single category (category name)
update     | 0                                               | Update existing schema (1) or keep existing files (0)

In the default situation the default schema is installed in ``/${RODSZONE}/yoda/schemas/default``.

Example invocation to install (or update) schema 'default' for all categories:
```bash
irule -F install-metadata-schema.r '*resc="irodsResc"' '*src="/etc/irods/irods-ruleset-research/tools/schemas/"' '*schema="default"' '*category="default"' '*update=1'
```

Example invocation to install (or update) schema 'test' for category 'experimental':
```bash
irule -F install-metadata-schema.r '*resc="irodsResc"' '*src="/etc/irods/irods-ruleset-research/tools/schemas/"' '*schema="test"' '*category="experimental"' '*update=1'
```

If you want to install individual files without the script then you can use the iput command.
If you install the files in a directory with the same name as the name of a category it will become the schema for that category and that category alone, when the category is created afterwards. Existing categories without a specific schema will still use the default schema.
To update existing files use the force flag "-f".
See the example below. Please replace `${RODSZONE}` with the current iRODS Zone and `${CATEGORY}` with the category you want to install.

```bash
iput -f metadata.json /${RODSZONE}/yoda/schemas/${CATEGORY}/metadata.json
iput -f research.xsd /${RODSZONE}/yoda/schemas/${CATEGORY}/research.xsd
iput -f vault.xsd /${RODSZONE}/yoda/schemas/${CATEGORY}/vault.xsd
iput -f avu.xsl /${RODSZONE}/yoda/schemas/${CATEGORY}/avu.xsl
iput -f datacite.xsl /${RODSZONE}/yoda/schemas/${CATEGORY}/datacite.xsl
iput -f landingpage.xsl /${RODSZONE}/yoda/schemas/${CATEGORY}/landingpage.xsl
```

The above is legal bash if you define the `CATEGORY` and `RODSZONE` environment variables, for example:

```bash
export CATEGORY=default
export RODSZONE=tempZone
```

Mistakes are easily made as the commands are so similar, but different.
So please take care.
