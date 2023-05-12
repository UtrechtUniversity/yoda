---
grand_parent: Software Design
parent: System Overview
nav_order: 4
---
# Statistics module

## Change in focus of statistics module
Starting from yoda release 1.8 the statistics module gives deeper insight in storage consumption. From this release storage is broken down in research, revision and vault storage.
In all previous yoda versions the storage consumption was related to resource tiers. This approach has been discarded following up requests made from within the yoda community.

In order to enable this new way of registering storage amounts two the following had the be taken care of:

1. the storage collection job had to be redesigned

2. Preservation of the already present (tier based) storage history.



## Storage collection job - nieuw
### Changes in collection of storage
Where yhe original job was based on a monthly premise and with a maximum of 12 months back, the new job however will be able to run anytime. This, with a minimum resolution of daily probes.  
Where the original job was limited to a 12 month cyclic buffer, making it impossible to record for more than 1 year of historic data, the new collection method has no limit in registering storage data anymore.  
In other words the entire storage history will be kept safely during the lifetime of the yoda-instance.

### Changes in storage type
Where the formally registered storage data that was fully tier based, in the new yoda-version a differentiation is created in collecting storage data for the research area, revisions area and vault area.  
Thus enabling the statistics module to show (historic) tables and graphs differentiating storage areas (research, revision, vault and totalized amounts).

## Transformation of original storage data
In order to safeguard the already present storage history it is required to be transformed to the new data structure.
Due to the limitation that it was registered tier-based, it is unclear to which area (research, revisions or vault) the data actually belongs to.  
Therefore, the transformed tier-based data is added to the 'totalized'-data and presented that way in the Statistics module



## Registering usage data
In previous yoda-versions a cronjob registers, once a month, all storage data for each category, based upon each group in the corresponding category.  
Starting from yoda-version 1.8 the collection job can be run any moment with a daily basis as a minimum resolution.  

Collection of storage amount is performed per group and is differentiated in research, revision and vault data for that group. And consequently stored as metadata on corresponding group.

All determined storage data is recorded on its corresponding group level.
Each group holds the following metadata with key: `org_storage_totals`.

This is postfixed with the month number, like:
```
org_storage_totals2023_05_01
org_storage_totals2023_05_02
org_storage_totals2023_05_03
```


Per entry (i.e. per group) storage information is held in a JSON format:

``['Categoryname', 'research value','vault value', 'revisions value', 'totalized value']``.


Metadata attribute:
`UUORGMETADATAPREFIX ++ 'storage_totals' ++ '2023_05_01';`

Metadata value:
`*json_str = "[\"*category\", 100, 200, 300, 600]";`

where in this example:
research = 100,  
vault = 200,  
revisions = 300  
and grand total = 600

The corresponding category is registered on group level as well as a group could possibly change category. So for historic purposes it is required to know to what category a group belonged.



## Collecting data for reporting
To find all latest and historic data for a category metadata can be matched against `‘[\“’ ++ *cat ++ ‘\”%%’`.
This will bring up all metadata storage metadata for this category.
