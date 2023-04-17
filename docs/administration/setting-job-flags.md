---
parent: Administration Tasks
title: Setting job flags
nav_order: 14
---
# Setting job flags
The replication and revision jobs can be graciously stopped by setting a flag.
When these flags are set, iRODS-level changes can be performed without having to kill these jobs (which can potentially cause inconsistencies / unexpected problems).
The jobs check for the presence a flag before processing each data object.
If it is present, the job stops and logs a message that it is stopped.

## For version <= 1.8

### Replication flag
Set:
```bash
itouch /tempZone/yoda/flags/stop_replication
```

Unset:
```bash
irm /tempZone/yoda/flags/stop_replication
```

### Revisions flag
Set:
```bash
itouch /tempZone/yoda/flags/stop_revisions
```

Unset:
```bash
irm /tempZone/yoda/flags/stop_revisions
```

## For version > 1.8

### Replication flag

Set:
```bash
imkdir /tempZone/yoda/flags/stop_replication
```

Unset:
```bash
irm -r /tempZone/yoda/flags/stop_replication
```

### Revisions flag
Set:
```bash
imkdir /tempZone/yoda/flags/stop_revisions
```

Unset:
```bash
irm -r /tempZone/yoda/flags/stop_revisions
```