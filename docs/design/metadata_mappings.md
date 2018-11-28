## Mapping of yoda-metadata.xml

When a datapackage with yoda-metadata.xml is published it will be processed and converted to three different forms.
If changes are made to the metadata.json or corresponding vault XSD, these processes could fail.

### XSLT for landing page
The landing page is generated with a extensible stylesheet.
Every new or changed element needs a template definition and a place in the group definition.
This stylesheet is named default2landingpage.xsl or named after category it applies to.
For example: ilab2landingpages.xsl.
This stylesheet should be put in the /zone/yoda/xsl collection.

### XSLT for DataCite
For DataCite a XML conforming to the DataCite Schema v4 is generated with an extensible stylesheet.
The mapping is documented outside this document.
This stylesheet is named default2datacite.xsl or named after the category it applies to.
For example: ilab2datacite.xsl.
This stylesheet should be put in the /zone/yoda/xsl collection.

### OAI-PMH importer
The OAI-PMH stream is updated by loading the yoda-metadata.xml with a Python script.
This Python script only looks for a couple of elements that map to Dublin core and DataCite.
Any changes to these fields will omit this metadata from the stream.
The mapping is documented outside of this document.

