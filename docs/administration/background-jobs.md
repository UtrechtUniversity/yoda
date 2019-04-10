# Long-running background jobs
Yoda can have long-running background jobs. Such jobs work on large amounts of
data in (small) batches, where the next batch is started through a delayed rule.
Currently there are two such jobs:

* iiCheckMetadataXmlForSchemaUpdates

  started by: `irods-ruleset-research/tools/check-metadata-for-schema-updates.r`

  Verify/update the metadata schemas of packages.

  Check with: `iqstat -a | grep iiCheckMetadataXmlForSchemaUpdates`

* uuCheckVaultIntegrity

  started by: `irods-ruleset-uu/tools/check-vault-integrity.r`

  Verify the checksums of all stored data.

  Check with: `iqstat -a | grep uuCheckVaultIntegrity`
