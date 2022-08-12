---
parent: Administration Tasks
title: Configuring cleanup functionality temporary files
nav_order: 13
---
# Configuring cleanup functionality of temporary files
This page contains instructions for configuring the cleanup feature in the research module. This feature
helps users find and remove files that should not be archived or published.

## Background
Some software automatically creates temporary, cache or metadata files.
For example, Windows Explorer can automatically create [Windows thumbnail cache files](https://en.wikipedia.org/wiki/Windows_thumbnail_cache)
that contain cached thumbnails of images. Such files should typically
not be archived or published. Removing these files manually is cumbersome, so Yoda has a cleanup tool
that enables users to find these files easily and optionally remove them.

Yoda searches for these files using a set of filename selection masks, such as wildcards.
The selection masks are configured at a system-wide level by the system administrator.

## Defining selection masks
Selection masks are used to match a type of file by its name.

### Mask - find specific files
It is possible to search for files that have a specific name.

For example:
```
    mask definition: 'Thumbs.db'
```
This mask will match files named 'Thumbs.db'.

### Mask - use of wildcards
It is possible to use all common wildcards in the creation of a mask.

For example:
```
    mask definition using wildcard:  '.*''
```

This mask will match files with a name starting with '.'.

### Multiple masks
Masks can be concatenated with a comma.

For example:
```
    multiple masks in mask definition: '.*','Thumbs.db'
```

## Configuring the variable
When creating a new Yoda instance, set variable 'temporary_files' in the group\_vars,
 as explained in [Configuring Yoda](configuring-yoda.md) and run the playbook.


## Default selection masks
By default, Yoda uses these selection masks:

- '._*'         # MacOS resource fork  
- '.DS_Store'   # MacOS custom folder attributes  
- 'Thumbs.db'   # Windows thumbnail images

## Usage

In the research space action menu in the Yoda portal, select the option 'Cleanup temporary files'.
