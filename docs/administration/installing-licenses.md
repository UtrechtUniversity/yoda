---
parent: Administration Tasks
title: Installing Licenses
nav_order: 3
---

# Background

Researchers can specify the license of a data package in its metadata. They can either use a standard
license (e.g. _Creative Commons Attribution 4.0 International Public License_), or use a custom license.

If the metadata of a data package specifies the name of a standard license (i.e. any license other than _Custom_), Yoda will include
the license text in a License.txt file in the root of the package when it is copied to the vault. The URI of the license
will be included in the metadata.

# Installing licenses

This section explains how to upload license texts and URIs, so that Yoda can automatically include them in data
packages.  In the example commands below, replace ${RODSZONE} with the iRODS zone name. Replace ${LICENSE} with
the name of the license, as defined in the metadata schema.

Yoda will look for the license text in _/${RODSZONE}/yoda/licenses/${LICENSE}.txt_ and for the license URI in
_/${RODSZONE}/yoda/licenses/${LICENSE}.uri_.

## Installing default licenses

The files of the licenses included in the default metadata schema can be found in _/etc/irods/irods-ruleset-uu/licenses_. The command to upload these license
files to Yoda is:

```bash
iput -r /etc/irods/irods-ruleset-uu/licenses /${RODSZONE}/yoda
```

## Installing non-default licenses

Put the license text in a file named _${LICENSE}.txt_. The _{LICENSE}.txt_ file needs to be pure ASCII, in order to
ensure it will be displayed correctly on every operating system and in every browser[^1]. The license URI should be
in a file named _${LICENSE}.uri_.

```bash
iput "${LICENSE}.txt" "/${RODSZONE}/yoda/licenses/${LICENSE}.txt"
iput "${LICENSE}.uri" "/${RODSZONE}/yoda/licenses/${LICENSE}.uri"
```

# Footnotes

[^1]: UTF-8 is not an option, because browsers will display a .txt file with the windows-1252 encoding. The ANSI subset of
the windows-1252 encoding is not an option, because Mac and linux will not correctly detect ANSI in a .txt file if opened
from the web disk.
