---
grand_parent: Software design
parent: Processes
---
# Folder Locking mechanism
To prevent modification of a folder in the research area, a researcher can use the lock function. This will catch attempts to write or remove data to that folder
until the folder is unlocked again. The same mechanism is used to prevent modification during the status transitions needed to put a folder in to the vault. The
iRODS ACL system could not be used, because researcher should be able to lock/unlock a folder themselves and not rely on an administrator to do so. This document describes
the technical implementation of the locking mechanism in the research ruleset.


Locks are represented by metadata on the folder, it's children and it's parents. The lock consists of a AVU with org_lock (defined in iiConstants.r) as attribute name and the collection where
the lock is started (rootCollection). Whenever a lock is set this AVU is put on every child using a treewalk and every parent using iteration until the ``/{rodsZone}/home/research-{groupName}`` collection is found. Every relevant static Policy Enforcement Point that could be triggered because of a modification in the research area is checked for the metadata and in general the following rules are enforced:

- if the root collection of the lock is on the current collection or a parent collection disallow the action.
- if the root collection of the lock is on a child collection allow modification of data objects, but disallow renames of parent collections.

In case there is a source and destination object, both need to be checked for locks and the following rules apply:

- if the source is locked, but the destination is not then disallow move operations, but allow copy operations.
- if the destination is locked, disallow every action.

msiOprDisallowed and msiDeleteDisallowed are used to stop the current operation and return an error to the clients.
There is one unfortunate special case. There is no static PEP for preconditions on a file put operation, only a post PEP. To prevent
users from putting new files into a locked collection the files are removed in the post condition `acPostProcForPut`. When using webDAV it may appear like the file is still there due to caching.


## Setting and removing locks
The locks are set and removed with the iiFolderLockChange rule in the iiFolderStatusTransition.r file.
This rule should not be directly run, but triggered from folder status transitions.
Please refer to the folder status design document for details on which transition should lock the folder.
The rules in iiFolderStatusTransitions.r called by the front-end to initiate a status change will attempt a metadata change on the `org_status` attribute.
This will trigger an metadata PEP, which will run the lock change when the current user is allowed to.
Every folder status transition is checked for preconditions by the iiCanModifyFolderStatus rule in iiPolicyChecks.r.

When the locking fails, the modification of the `org_status` change will be interrupted by calling msiOprDisallowed.
For the rules called by the front-end the errors are caught and returned with statusInfo.
