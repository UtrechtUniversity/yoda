# Statistics module

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
