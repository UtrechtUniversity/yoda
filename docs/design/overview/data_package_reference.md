---
grand_parent: Software Design
parent: System Overview
nav_order: 11
---
# Data Package Reference

The Data Package Reference is available from the moment the a Data Package has been submitted into the Vault Space
This reference can be used to communicate with other users and refer to the Data Package and making references to existing Data Packages, when archiving a new Data Package.

The reference is be globally unique and leads to the Vault Space for that Data Package.
An example Data Package Reference is `yda/2bb04907-97cb-4a35-bc68-b56025bee47e`.
An example of a complete link to this Data Package would be `https://portal.yoda.test/vault/yda/2bb04907-97cb-4a35-bc68-b56025bee47e`.

## Adding Data Package Reference to existing vault packages
To add the Data Package Reference to existing vault packages without a reference is script is available:

```bash
irule -r irods_rule_engine_plugin-python-instance -F /etc/irods/yoda-ruleset/tools/generate-data-package-references.r
```
