---
title: Naming conventions
parent: Software Design
nav_order: 4
has_children: true
has_toc: false
---
# Naming conventions

Yoda entities such as collections, data objects, categories, groups, etc. have certain naming requirements and restrictions. These exist either because of structural limitations of certain parts of the system, or to avoid errors and/or malfunctions of the system. This part of the documentation lists all the requirements and restrictions that should be followed when naming the Yoda entities.

## Collection and data object names

System limitations to take into considerations:

- iRODS has a maximum path length of 1024 bytes[^1] (see: [iRODS maximum path length allowed](https://github.com/irods/irods/blob/4669cd6be829ed7bc3a4c6648b7eac408839e647/lib/core/include/irods/rodsDef.h#L42)).
- If any member of your group(s) use Windows native WebDAV, the WebDAV part of the paths of each data object and collection should be limited to 260 characters (due to [Windows systems maximum path length limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry)).

In addition to these, there are some known naming issues that should also be taken into consideration:

- Collection names containing single apex quote `'` cause issues (see: [irods/irods#5727](https://github.com/irods/irods/issues/5727)).
- Renaming of collection names containing multi-byte characters mangles subcollection paths (see: [irods/irods#6239](https://github.com/irods/irods/issues/6239)).
- Data object names containing non-standard characters (such as control characters with ASCII codes 01 to 08, 11, 12, 14 to 31) cause encoding issues in XML (see: [irods/irods#4132](https://github.com/irods/irods/issues/4132#issuecomment-528786460)).

## User names

Rules for user names are as follows:

- must contain zero or one '@' symbol, but not at the beginning or the end of the name;
- (if '@' symbol is not present) must contain only lowercase letters, and dots;
- (if '@' symbol is present) must contain only lowercase letters, numbers, hyphens, underscores, and dots;
- may contain a zone name after a '#' symbol.

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L23-L35), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L43-L50)

## Group names

Rules for group names are as follows:

- must be prefixed with 'research-' or 'deposit-';
- must contain only lowercase characters, numbers, and hyphens;
- must not start or end with a hyphen;
- must not exceed 63 characters.

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L37-L55), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L33-L40)

## Category names

Rules for category names are as follows:

- must contain only lowercase characters, numbers, and hyphens;
- must not start or end with a hyphen;
- must not exceed 2700 bytes[^1].

Despite the 2700-byte length limitation, it is strongly advised not to exceed 63 characters as longer names would be hard to read in the Group Manager module.

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L57-L64), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L13-L20)

## Subcategory names

Rules for subcategory names are as follows:

- must contain only letters, numbers, spaces, commas, periods, parentheses, underscores, and hyphens;
- must not exceed 2700 bytes[^1].

Despite the 2700-byte length limitation, it is strongly advised not to exceed 63 characters as longer names would be hard to read in the Group Manager module.

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L66-L75), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L23-L30)

## Licenses

Detailed information regarding default and non-default licenses can be found in the [Installing licenses](/../../administration/installing-licenses.md) page.

# Footnotes

[^1]: Number of bytes directly translates to number of characters, only in case of single-byte characters.