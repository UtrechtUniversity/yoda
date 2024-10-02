---
parent: Administration Tasks
title: Troubleshooting published data packages
nav_order: 21
---

# How to Troubleshoot Published Data Packages

To diagnose issues with existing published data packages, the tool performs a series of checks to verify the integrity and compliance of data packages.

**Requirement:** Python 3 or higher required.

---

### **Check Steps**

The tool performs the following checks:

1. **Metadata Schema Conformance:**
   - Verifies that the metadata of each data package conforms to the associated schema.

2. **System AVUs Verification:**
   - Checks whether each data package has the expected system Attribute-Value Units (AVUs).

3. **DOI Registration Status:**
   - Checks the registration status of both `versionDOI` and `baseDOI` from the DataCite API.

4. **Landing Page Integrity:**
   - Compares the contents of the local landing page file with the remote version in public server to ensure they match.

5. **Combined JSON Integrity:**
   - Checks the integrity of the combined JSON file by verifying its URL online and confirming the existence of the file.
   - In offline mode, it only checks whether the `combi_json` file exists locally.

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
e.g, research-initial[1725262507]

### **3. Log results and offline mode**
By default, the results are displayed in terminal (stdout). Furthermore, to save the detailed output to a log file executre:
```bash
python3 troubleshoot-published-data.py -l -o
```
- The -l option enables logging mode.
- The -o option enables off mode, which skips several tests related to connecting to remote server. 

e.g, research-initial[1725262507]
## Note
For more info, see...(design) documentation 
TODO: go over the codes and jira text for better understanding 

How does PUBLISHED defined. 

TODO: add output log location and server log, and terminal 

TODO: add example of output 
