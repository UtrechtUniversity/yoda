# Installing metadata schemas, formelements and stylesheets
For a fully functional research module, a number of XML schema's and stylesheets are required.
Currently we only have a default schame (currently the same as the I-lab schema) and a test schema.
These can be found in the irods-ruleset-research in `tools/xml/`.
Below a description of the needed files (using the default schema as example):

**default.xsd**
  A schema describing the elements and their type of a yoda-metadata.xml

**default.xml**
  An XML file describing the formelements and grouping of elements corresponding to the elements in the XSD

**default.xsl**
  A stylesheet to convert a yoda-metadata.xml to a AVU XML that can be loaded into iRODS with msiLoadMetadataFromXML(Buf)

**default2datacite.xsl**
  A stylesheet to convert a combi.xml consisting of user metadata from a yoda-metadata.xml file and system metadata into
  the DataCite XML format

**default2landingpage.xsl**
  A stylesheet to convert a combi.xml into a landing page html file

**schema-for-formelements.xsd**
  A schema to check the validity of a uploaded formelements file

**schema-for-xsd.xsd**
  A schema to validate XSD schema's.

You can install this set with the `tools/install-default-xml-for-metadata.r` script. This script accepts four parameters:
resc, src, default and update.


Parameter  | Default value                               | Description
-----------|---------------------------------------------|------------
resc	     | irodsResc	                                 | Default resource to put the files into
src        | /etc/irods/irods-ruleset-research/tools/xml | Source directory of files
default    | default                                     | Category to use as default (default or test).
update     | 0                                           | Update existing XSD, XML, XSL (1) or keep existing files (0)

In the default situation every schema name, for example `custom{.xsd,.xml,.xsl}` file will become `default{.xsd,.xml,.xsd}` file in the right collection.

Example invocation:
```bash
irule -F install-default-xml-for-metadata.r '*resc="irodsResc"' '*src="/etc/irods/irods-ruleset-research/tools/xml/"' '*default="default"' '*update=1'
```

If you want to install individual files without the script then you can use the iput command.
If you install the file as the name of a category it will become the schema for that category and that category alone.
To update existing files use the force flag "-f".
See the example below. Please replace `${RODSZONE}` with the current iRODS Zone and `${CATEGORY}` with the category you want to install.

```bash
iput -f ${CATEGORY}.xml /${RODSZONE}/yoda/formelements/${CATEGORY}.xml
iput -f ${CATEGORY}.xsd /${RODSZONE}/yoda/xsd/${CATEGORY}.xsd
iput -f ${CATEGORY}.xsl /${RODSZONE}/yoda/xsl/${CATEGORY}.xsl
iput -f ${CATEGORY}2datacite.xsl /${RODSZONE}/yoda/xsl/${CATEGORY}2datacite.xsl
iput -f ${CATEGORY}2landingpage.xsl /${RODSZONE}/yoda/xsl/${CATEGORY}2landingpage.xsl
```

The above is legal bash if you define the `CATEGORY` and `RODSZONE` environment variables, for example:

```bash
export CATEGORY=default
export RODSZONE=tempZone
```

Mistakes are easily made as the commands are so similar, but different.
One letter difference could put an XSL in the XSD collection, for example.
