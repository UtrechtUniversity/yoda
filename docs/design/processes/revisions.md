---
grand_parent: Software Design
parent: Processes
---
# Revision management

By default, Yoda stores revisions of data objects up to 2 GB, so that users can restore earlier versions of these data objects if needed.
The revision store is located at `/tempZone/yoda/revisions` (where `tempZone` is the zone name).

## Revision strategies

Yoda uses a _revision strategy_ that defines which revisions need to be kept. Revisions that don't need to be kept as per
this policy are removed by the daily revision cleanup job. A revision strategy consists of a series of successive time buckets, where
the first bucket starts in the present.  For example, in strategy `A` (see table below), the first bucket refers to all revisions
created in the last six hours, the second bucket refers to all revisions created in the twelve hours before that, and so forth.
Yoda uses strategy `B` by default.

If a data object has any revisions in a defined bucket, the cleanup job removes revisions that do not belong to any bucket. If a data object
has no revisions in a defined bucket, the cleanup job removed all but the last revision. This ensures that at least one revision of data object
is kept, so it can always be reverted to the previous version.

**Strategy A:**

time bucket | number of revisions
------------|---------------------
6 hours     | 1
12 hours    | 1
18 hours    | 1
1 day       | 1
2 days      | 1
3 days      | 1
4 days      | 1
5 days      | 1
6 days      | 1
1 week      | 1
2 weeks     | 1
3 weeks     | 1
4 weeks     | 1
8 weeks     | 1
12 weeks    | 1
16 weeks    | 1

**Strategy B:**

time bucket | number of revisions
------------|---------------------
12 hours    | 2
1 day       | 2
3 days      | 2
5 days      | 2
1 week      | 2
3 weeks     | 2
8 weeks     | 2
16 weeks    | 2

**Strategy Simple:**

time bucket | number of revisions
------------|---------------------
16 weeks    | 16
