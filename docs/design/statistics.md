# Statistics module

# Resources and tiers
Any resources can be administratively assigned to one tier.
A tier is an ilab-application introduced entity, not standard iRODS
A tier can be considered a price level of a resource.

metadata on resource level:`org_storage_tier  = ‘tape’`

If no tier is assigned to a resource yet, this is considered the ‘Standard’ tier by default.

# Registering usage data
Once a month a cronjob registers storage data for each category, based upon each group in the category.
Collection of storage amount is performed  per group and per storage tier and stored as metadata on corresponding group.

All determined storage data is recorded on group level.
Each group holds the following metadata with key: `org_storage_data_month`.

This is postfixed with the month number, like:
```
org_storage_data_month01
org_storage_data_month02
org_storage_data_month03
org_storage_data_month04
org_storage_data_month05
org_storage_data_month06
org_storage_data_month07
org_storage_data_month08
org_storage_data_month09
org_storage_data_month10
org_storage_data_month11
org_storage_data_month12
```
Thus creating a full year cyclic buffer.

Per entry, i.e. for a group every month, each metadata-entry holds category, tier and  storage information in a JSON format ``['Categoryname', 'Tiername', '100']``.
The frontend steps into this cyclic buffer starting from current month backward.
Per month the front end gets tiername and storage data in a total array divided in
tiername, months and storage.

Metadata attribute:
`UUORGMETADATAPREFIX ++ 'storage_data_month' ++ *month;`

Metadata value:
`*json_str = "[\"*category\", \"*tier\", \"*storageAmount\"]";`

The corresponding category is registered on group level as well as a group could possibly change category. So for historic purposes it is required to know to what category a group belonged.

# Twelve month registration
Per group one or more metadata attributes like this exist for a month.  
This occurs for each month (`org_storageDataMonth01, … , org_storageDataMonth12`) thus setting up a cyclic buffer for registration with a maximum history  12 months history.
After 12 months the previous values are overwritten automatically by the mothly cronjob.

# Collecting data for reporting
To find all latest and historic data for a category metadata can be matched against `‘[\“’ ++ *cat ++ ‘\”%%’`.
This wil bring up all metadata storage metadata for this category. Combined with a specific month this will bring up all required data to calculate  the storage per tier for a specific category for a month.

# Which month does registered data belong to?
For now, when registration takes place after the 15th of a month, the data collected is linked to the month later.
I.e. data collected on 27th of may is linked to the month of June. And therefore registered under `org_storage_data_month06`.
This as invoicing takes place in June over the month of may.
