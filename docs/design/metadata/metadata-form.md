---
grand_parent: Software Design
parent: Metadata
---
# Metadata form implementation

This page contains implementation information about the metadata form functionality.

## Form functionality

The metadata form handling is implemented in a generic manner.   
In itself the generic metadata form deals with two situations, i.e.
- an editable form in which users can edit/add metadata to a datapackage
- a readonly view on this metadata as previously entered by a researcher

The generic (metadata) form deals with:
- Presenting a form for the metadata of a specific datapackage where the elements on the form are configurable dependent on category
- A default metadata form configuration when no metadata form configuration exists for a category or group
- Possibility to have dependencies between elements on the form in order to form clear relations between the data
- Determining completeness of the form and giving proper indications to the user dependent on the category a datapackage belongs to
- Determining validity of the metadata form data dependent on the category a datapackage belongs to
- Saving the metadata to a file in JSON format within the datapackage (`yoda-metadata.json`)
  This file can also be edited by regular users.
- When data is saved correctly, copy the metadata to AVUs so that metadata can be searched by users.
- Offering possibilities to, after correctly/successfully validating a metadata set, the result can be used for further actions.  Like the ability
    - to bring a datapackage / metadata to the vault from within the dynamic storage environment
    - to save several metadata files, with unique names, within the vault
- readonly view on metadata for a datapackage

## Integration of React form within Yoda

The directory `/research/metadata-form/src` in the Yoda portal repository contains Yoda-specific javascript code for the React form.
