---
grand_parent: Software Design
parent: Processes
---
# Revision management

For each new file or file modification Yoda creates a timestamped backup file in the revision store. The revision store is located at `/tempZone/yoda/revisions`.

## Revision strategies
Not all revisions are kept, only a predefined number of revisions are being kept per time bucket.
A time bucket is a time offset from now into the past.
Each revision strategy has a predefined set of time buckets and number of revisions stored in those buckets.

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
16 weeks    | 5
