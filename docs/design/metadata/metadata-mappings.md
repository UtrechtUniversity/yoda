---
grand_parent: Software Design
parent: Metadata
---
## Metadata mappings
When a datapackage with yoda-metadata.json is published it will be processed and converted to three different forms.
If changes are made to the metadata.json.

### Jinja2 template for landing page
The landing page HTML code is generated using a Jinja2 template. This template may need to be adapted
in case of metadata schema changes. The template can be found in
`/etc/irods/irods-ruleset-uu/templates/landingpage.html.j2`. The Ansible playbook activates this template
by uploading it to the `/zone/yoda/templates/` collection.

### JSON generator for DataCite
For DataCite a JSON-file is generated conform the DataCite Schema v4.  
This generator can be found in `/etc/irods/yoda-ruleset/json_datacite41.py`.

### OAI-PMH importer
The OAI-PMH stream is updated by loading the yoda-metadata.json with a Python script.
This Python script only looks for a couple of elements that map to Dublin core and DataCite.
Any changes to these fields will omit this metadata from the stream.
The mapping is documented outside of this document.
