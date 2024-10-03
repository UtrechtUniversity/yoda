---
parent: Administration Tasks
title: Troubleshooting published data packages
nav_order: 21
---
# How to troubleshoot published data packages

This documentaion explains how users can diagnose issues with all existing published data packages, the tool performs a series of checks to verify the integrity and compliance of data packages. This published data packages include data with status (?what AVU) that is published (?format), or failed-to-published packages (AVU status = unpublished ?format).

**Requirement:** Python 3 or higher required, Yoda version 1.10 or later, rodsadmin privilege

## **Check Steps**

The tool performs the following checks:

### **Metadata Schema Conformance**

This step verifies that the metadata of the data package conforms to the associated schema.


### **System AVUs Verification:**

This step checks whether the data package has the expected system Attribute-Value Units (AVUs). This is done by comparing AVUs starting with `publication_` (format?) compling with groud truth AVU keys, consequently, the check results reveal if there are missing AVUs or unexpected AVUs. If there were, will be printed to terminal and logfile. 

### **DOI Registration Status:**

This step checks the registration status of both `versionDOI`(if there are) and `baseDOI` from the DataCite API. This is done by checking `versionDOI`  and `baseDOI` from metadata AVUs of the package are registered or not in DataCite by sending a API request to access this DOI in DataCite. 

4. **Landing Page Integrity:**

This step Compares the contents of the local landing page file with the landingpage in remote server to ensure they match. This is done by sending a url request to download content from landingpage of the data package, and compare the content with the local landingpage html file. Note, enable off line mode if no internet connection. In off_line (format?) mode, this step checks if there are content in the local landing page url, but it does not verify the correctness of the content. 

5. **Combined JSON Integrity:**

This step Checks the integrity of the combined JSON file by verifying its URL online and confirming the existence of the file. 

This is Done by checking the metadata json sent to OAI-PMH, for if they can be found in OAI-PMH. 

In offline mode, it only checks whether the `combi_json` file exists locally.

---

## Commands

The tool can be used with various options as detailed below.

### **1. General Check**

To perform checks on all published data packages:

```bash
python3 troubleshoot-published-data.py
```

### **2. Specific Package Check**

To inspect a single data package:

```bash
python3 troubleshoot-published-data.py -p <package-name>
```

An example of data package name" `research-core-0[1722266819]`

### **3. Log results and offline mode**

By default, the results are displayed to terminal (stdout). Furthermore, to save the detailed output to a log file execute:

```bash
python3 troubleshoot-published-data.py -l -o
```

- The -l option enables logging mode. Saving log to `/var/lib/irods/log/troubleshoot_publications.log"`
- The -o option enables off mode, which skips several tests related to connecting to remote server.


### Example output:
For a single package check 

Failed case: 
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

Success case:

TODO: add
