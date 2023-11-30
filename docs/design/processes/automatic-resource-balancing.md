---
grand_parent: Software Design
parent: Processes
---

# Automatic Resource Balancing

This page contains information about Automatic Resource Balancing (ARB), the process that Yoda optionally uses to ensure that newly
created data objects are stored on iRODS resources that still have enough space available.

## Background

One of the functions of iRODS is to facilitate storage abstraction: data can be stored on different types of back-end storage (e.g. object
storage, NFS shares, etc), but is presented to the user in a unified way. iRODS keep track of storage areas, such as local filesystems or
object storage buckets, as resources. Some resources can be scalable (e.g. object storage), whereas other are not scalable in practice
(e.g. local filesystems, depending on the infrastructure).

## Problem description

When a non-scalable storage resource does not have enough space left for new data objects, iRODS needs to be configured to not store
any new data on it, in order to prevent failures due to the resource running out of space. On environments with a small number of resources,
manually moving resources out of the iRODS tree is workable, however this becomes cumbersome and prone to errors as the number of resources grows.
Relying on manual administrator action also increases the risk that a resource will fill up outside of office hours, before an administrator
has had time to move it out of the tree.

Furthermore, moving resources out of the tree causes problems with writes to existing objects. We need to enforce a default resource on uploads of
new files in order to be able to enforce a replica policy (e.g. a data object should have one replica in each of two datacenters). However, when a full
resource is moved out of the tree, the default resource no longer matches with existing data objects on that resource, which results in errors when a user
tries to update existing data objects. In order to resolve this issue, we need to keep full resources in the trees.

iRODS has a built-in mechanism for enforcing minimum free space on unixfilesystem resources: the
[minimum_free_space_for_create_in_bytes setting](https://docs.irods.org/4.2.12/plugins/composable_resources/#unixfilesystem). However, as of iRODS 4.2.12,
this setting is incompatible with Python-iRODS-client (see e.g. https://github.com/irods/python-irodsclient/issues/462 and https://github.com/irods/irods/issues/7154).
Therefore it is currently not usable in Yoda.

Considering that we need to determine which resources are full on every data object creation, we need a solution that is optimized for
frequent lookups.

## Solution

The current solution for this problem in Yoda is automatic resource balancing (ARB). It consists of the following parts:
- All iRODS systems in the zone (both provider and consumer) have a local cronjob named `arb-update-resources` that periodically retrieves
  total and available space for every local unixfilesystem resource. This information is submitted to an update rule in the ruleset.
- The update rule compares available space to a relative trigger value (configuration setting `irods_arb_min_percent_free`) and absolute
  trigger value (configuration setting `irods_arb_min_gb_free`), and checks whether the resource has been
  manually configured to be exempt from ARB (configuration setting `irods_arb_exempt_resources`). Based on this, resources
  are assigned one of the following ARB values:

  * IGNORE: this resource is irrelevant to ARB, because it is not a passthrough parent resource of a
    unixfilesystem resource.
  * EXEMPT: this resource has been manually configured to be ignored by ARB.
  * FULL: ARB applies to this resource; it has exceeded one of the trigger values
  * AVAILABLE: ARB applies to this resource; it has not yet exceeded one of the trigger values.

  These values are stored in both a Redis data structure store and a resource AVU. The Docker setup currently does not have a Redis store, so uses AVUs only if ARB is enabled.
- When ARB is enabled, the `pep_resource_resolve_hierarchy_pre` policy retrieves the ARB value of a resource on create actions. It applies a write
  vote of `0.0` if the ARB value is `FULL`. If possible, the policy retrieves the ARB value from Redis; there is also a fallback lookup that uses 
  the resource AVU.

Together, these components ensure that a resource does not get votes for creating new data objects after it has exceeded one of the trigger values
for minimum amount of free space.

## Limitations

- ARB checks available space once a minute by default. The configured trigger values need to take into account that some time can pass between
  a resource exceeding its minimum amount of free space, and ARB detecting this event.
- ARB only affects creation of new data objects. Expansion of existing data objects is not considered. This needs to be taken into account
  when choosing trigger values.
- ARB can currently only process unixfilesystem resources. Other storage resources are ignored.
