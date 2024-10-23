---
parent: Administration Tasks
title: Troubleshooting published data packages
nav_order: 21
---
# How to troubleshoot published data packages

This documentation explains how users can diagnose issues with all existing published data packages using our new troubleshooting tool. The tool performs a series of checks to verify the integrity and compliance of data packages. The scope of this tool includes both data packages that have been successfully published and those that have failed to publish (packages that initiated the publication process but did not succeed). Specifically, it targets data packages with their Attribute-Value Units (AVUs) including `org_publication_status` of `OK`, `Retry`, `Unrecoverable`, or `Unknown`. Note, the `org_` prefix may vary in different Yoda instance as it is a constant variable of `UUORGMETADATAPREFIX` stored in `constant.py`

Alternatively, the tool can diagnose a specific data package when provided with its name.

**Requirement:** Python 3 or higher required, Yoda version 1.10 or later, rodsadmin user

## Check Steps

The tool performs the following checks:

### Metadata Schema Conformance

This step verifies that the metadata of the data package conforms to the associated schema.


### System AVUs Verification

This step checks whether the data package has the expected system Attribute-Value Units (AVUs). It does this by comparing AVUs that start with `org_publication` against the expected AVU keys (ground truth). The check results reveal if there are missing or unexpected AVUs, which will be printed to the terminal and the logfile.

### DOI Registration Status

This step checks the registration status of both `versionDOI` (if available) and `baseDOI` using the DataCite API. It retrieves the DOIs from the package's metadata AVUs and sends API requests to DataCite to verify if these DOIs are registered.

### Landing Page Integrity

This step compares the contents of the local landing page file with the remote landing page to ensure they match. It does this by sending a URL request to download the HTML of the data package's landing page and comparing it with the local HTML file. Note that if there is no internet connection, you should enable the `offline` mode. In offline mode, this step checks if the local landing page file exists but does not verify the correctness of its content.

### Combined JSON Integrity

This step checks the integrity of the combined JSON file by verifying its URL online and confirming the existence of the file. It accomplishes this by checking if the metadata JSON sent to OAI-PMH server can be found in the OAI-PMH repository. In offline mode, it only checks whether package's `-combi.json` file exists locally


## Commands

The tool can be used with various options as detailed below.

### 1. General Check

To perform checks on all published data packages:

```bash
python3 troubleshoot-published-data.py
```

### 2. Specific Package Check

To inspect a single data package:

```bash
python3 troubleshoot-published-data.py -p <package-name>
```

An example of data package name is `research-core-0[1722266819]`

### 3. Log results and offline mode

By default, the results are displayed to terminal (stdout). Furthermore, to save the detailed output to a log file execute:

```bash
python3 troubleshoot-published-data.py -l -o
```

- The -l option enables logging mode. Saving log to `/var/lib/irods/log/troubleshoot_publications.log`
- The -o option enables offline mode, which skips several tests related to connecting to remote servers. This is useful when testing on a local development environment.
- The -n option enables no datacite mode, which skips the datacite checks. This is also useful when testing on a local development environment.

## Example output

When checking a single data package, the output containing successful and failed checks displayed in the terminal is as follows:

```
Troubleshooting data package: /tempZone/home/vault-core-0/research-core-0[1722266819]
compare_local_remote_landingpage: File contents at irods path </tempZone/yoda/publication/JCY2C2.html> and remote landing page <https://public.yoda.test/allinone/UU01/JCY2C2.html> do not match.
Results for: /tempZone/home/vault-core-0/research-core-0[1722266819]
Package FAILED one or more tests:
Schema matches: True
All expected AVUs exist: True
No unexpected AVUs: True
Version DOI matches: False
Base DOI matches: False
Landing page matches: False
Combined JSON matches: True
```

For checks involving multiple data packages, the output for each package is aggregated, displaying the results consecutively in the terminal. This allows for a comprehensive view of the results across different packages.
