# Installing lists of preservable file formats
Preservable file formats are read from iRODS and presented to the user.
It needs to be a JSON (.json) file which validates against the JSON schema below.

The naming scheme is up to the administrator, the lists ar presented alphabetically.
In order for every user to be able to read the terms, a read ACL for public needs to be set.

```bash
iput -r /etc/irods/irods-ruleset-research/tools/file_formats /${RODSZONE}/yoda
ichmod -rM inherit  /${RODSZONE}/yoda/file_formats
ichmod -rM read public /${RODSZONE}/yoda/file_formats
```

To add a new list of preservable file formats just put a JSON file in the `/${RODSZONE}/yoda/file_formats` collection with a new name.

```bash
iput "${FILE_FORMATS}.txt" "/${RODSZONE}/yoda/file_formats/${FILE_FORMATS}.json"
```

JSON schema for preservable file formats:
```json
{
  "definitions": {},
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "preservable_file_formats.json",
  "type": "object",
  "title": "List of preservable file formats",
  "required": [
    "name",
    "formats"
  ],
  "properties": {
    "name": {
      "$id": "#/properties/name",
      "type": "string",
      "title": "File formats list name",
      "default": "",
      "examples": [
        "DANS Preferred formats"
      ],
      "pattern": "^(.*)$"
    },
    "formats": {
      "$id": "#/properties/formats",
      "type": "array",
      "title": "List of file formats",
      "default": null,
      "items": {
        "$id": "#/properties/formats/items",
        "type": "string",
        "title": "Preservable file formats",
        "default": "",
        "examples": [
          "pdf",
          "txt",
          "xml",
          "html",
          "css",
          "ods",
          "csv",
          "sql",
          "jpg",
          "tiff",
          "png",
          "svg"
        ],
        "pattern": "^(.*)$"
      }
    }
  }
}
```
