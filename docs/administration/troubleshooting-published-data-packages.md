---
parent: Administration Tasks
title: Troubleshooting published data packages
nav_order: 21
---
# How to troubleshoot published data packages

This documentation explains how users can diagnose issues with all existing published data packages using our new troubleshooting tool. The tool performs a series of checks to verify the integrity and compliance of data packages. The scope of this tool includes both data packages that have been successfully published and those that have failed to publish (packages that initiated the publication process but did not succeed). Specifically, it targets data packages with their Attribute-Value Units (AVUs) including `org_publication_status` of `OK`, `Retry`, `Unrecoverable`, or `Unknown`. Note, the `org_` prefix is defined by the constant variable of `UUORGMETADATAPREFIX` stored in `constants.py` in the ruleset.

Alternatively, the tool can diagnose a specific data package when provided with its name.

**Requirements:**
- Python 3 or higher
- Yoda version 1.10 or later
- Script must be run as rodsadmin user

## Check Steps

The tool performs the following checks:

### Metadata Schema Conformance

This step verifies that the metadata of the data package conforms to the associated schema.


### System AVUs Verification

This step checks whether the data package has the expected system Attribute-Value Units (AVUs). It does this by comparing AVUs that start with `org_publication` against the expected AVU keys (ground truth). The check results reveal if there are missing or unexpected AVUs, which will be printed to the terminal and the log file.

### DOI Registration Status

This step checks the registration status of both `versionDOI` (if available) and `baseDOI` using the DataCite API. It retrieves the DOIs from the package's metadata AVUs and sends API requests to DataCite to verify if these DOIs are registered.

### Landing Page Integrity

This step compares the contents of the local landing page file with the remote landing page to ensure they match. It does this by sending a URL request to download the HTML of the data package's landing page and comparing it with the local HTML file. Note that if there is no internet connection, you should enable the `offline` mode. In offline mode, this step checks if the local landing page file exists but does not verify the correctness of its content.

### Combined JSON Integrity

This step checks the integrity of the combined JSON file by verifying its URL online and confirming the existence of the file. It accomplishes this by checking if the metadata JSON sent to OAI-PMH server can be found in the OAI-PMH repository. In offline mode, it only checks whether package's `-combi.json` file exists locally


## Commands Execution Guide

The tool can be used with various options as detailed below. Ensure you are logged in as an irodsadmin user for the necessary permissions and navigate to the 'yoda-ruleset/tools' directory before running any commands, e.g.,

```bash
cd /etc/irods/yoda-ruleset/tools
```

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

The package can either be specified as the short name (the name of the folder that you see in the vault), for example `research-core-0[1722266819]`, or the path to the package, for example: `vault-core-0/research-core-0[1722266819]`. Be aware that if  the package short name contains spaces then the package must be specified in quotes.

### 3. Log results and offline mode

By default, the results are displayed to terminal (stdout). Furthermore, to save the detailed output to a log file execute:

```bash
python3 troubleshoot-published-data.py -l
```

- The -l option enables logging mode. This saves the log to `/var/lib/irods/log/troubleshoot_publications.log`
- The -o option enables offline mode, which skips several tests related to connecting to remote servers, but does not skip the datacite test. This is useful when testing on a local development environment.
- The -n option enables no datacite mode, which skips the datacite checks. This is also useful when testing on a local development environment.
- The -m option specifies output format: 'human' for readable text (default) or 'csv' for spreadsheet-ready data. 

## Example output

When checking a single data package, the output containing successful and failed checks displayed in the terminal is as follows. 

- In human-readable mode:

```
Troubleshooting Results for: /tempZone/home/vault-default-3/research-default-3[1744029023]
Package FAILED one or more tests:
Schema Check: Pass
Missing AVUs Check: Pass
Unexpected AVUs Check: Pass
Version DOI Check: Fail
Landing Page Check: Pass
Combi JSON Check: Pass
```

- In csv mode:

```
/tempZone/home/vault-default-3/research-default-3[1744029023],Pass,Pass,Pass,Fail,N/A,Pass,Pass
```

Note: "N/A" indicates checks skipped due to irrelevance (e.g., base DOI validation for packages without prior versions). And for checks involving multiple data packages, the output for each package is aggregated, displaying the results consecutively in the terminal. This allows for a comprehensive view of the results across different packages.
