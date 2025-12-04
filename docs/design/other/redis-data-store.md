---
grand_parent: Software design
parent: Other
---
# Redis key-value store

Yoda uses a Redis key-value store to store various internal
data. Please find an overview of the Redis databases below:

| Database number | Component | Feature                       |
| --------------- | --------- | ----------------------------- |
| 0               | Provider  | Automatic resource balancing  |
| 1               | Portal    | API Cache                     |
| 2               | Public    | Anubis storage                |

More information:
- [Automatic resource balancing](../processes/automatic-resource-balancing.md)
  is a process that takes care of balancing uploaded data across storage resources,
  taking into account available free space.
- The API cache is an optional feature that aims to improve performance
  of the Yoda portal by caching application data.
- Anubis is a feature to protect against aggressive web scrapers.
  This database keeps track of who has been verified as not a bot.
