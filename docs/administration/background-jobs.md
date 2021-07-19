---
parent: Administration tasks
title: Long-running background jobs
nav_order: 9
---
# Long-running background jobs
Yoda can have long-running background jobs. Such jobs work on large amounts of
data in (small) batches, where the next batch is started through a delayed rule.
Currently there are two such jobs:

* iiCheckMetadataXmlForSchemaUpdates

  started by: `irods-ruleset-research/tools/check-metadata-for-schema-updates.r`

  Verify/update the metadata schemas of packages.

  Check with: `iqstat -a | grep iiCheckMetadataXmlForSchemaUpdates`

  All metadata touched will be logged in the rodsLog.

  Adding the schema identifiers can take some time, the batch script adds 256 jobs per 60 seconds to the rule queue.

* uuCheckVaultIntegrity

  started by: `irods-ruleset-uu/tools/check-vault-integrity.r`

  Verify the checksums of all stored data.

  Check with: `iqstat -a | grep uuCheckVaultIntegrity`

  All data objects with data itegrity issues are logged in the rodsLog.

  Checking the vault integrity takes a lot of time.

  To add minimal load on the system, the batch script adds 256 jobs per 60 seconds to the rule queue.
