---
grand_parent: Software Design
parent: Metadata
---
## Metadata mappings
When a datapackage with yoda-metadata.json is published it will be processed and converted to three different forms.
If changes are made to the metadata.json.

### Jinja2 template for landing page
The landing page HTML is generated with a Jinja2 template
Every new or changed element needs a template definitio.
This template is named landingpage.j2 and should be put in the `/zone/yoda/templates/` collection.

### XML generator for DataCite
For DataCite a XML conforming to the DataCite Schema v4 is generated in Python.
This generator can be found in `/etc/irods/yoda-ruleset/json_datacite41.py`.

### OAI-PMH importer
The OAI-PMH stream is updated by loading the yoda-metadata.json with a Python script.
This Python script only looks for a couple of elements that map to Dublin core and DataCite.
Any changes to these fields will omit this metadata from the stream.
The mapping is documented outside of this document.
