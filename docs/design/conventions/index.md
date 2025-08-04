---
title: Naming conventions
parent: Software Design
nav_order: 4
has_children: true
has_toc: false
---
# Naming conventions

Yoda entities such as collections, data objects, categories, groups, etc. have certain naming requirements and restrictions. These exist either because of structural limitations of certain parts of the system, or to avoid errors and/or malfunctions of the system. This part of the documentation lists all the requirements and restrictions that should be followed when naming the Yoda entities.

## User names

Rules for user names are as follows:

- must contain zero or one '@' symbol, but not at the beginning or the end of the name
- (if '@' symbol is not present) must contain only lowercase letters, and dots
- (if '@' symbol is present) must contain only lowercase letters, numbers, hyphens, underscores, and dots 
- may contain a zone name after a '#' symbol

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L23-L35), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L43-L50)

## Group names

Rules for group names are as follows:

- must be prefixed with 'research-' or 'deposit-'
- must contain only lowercase characters, numbers, and hyphens
- must not start or end with a hyphen
- must not exceed 63 characters

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L37-L55), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L33-L40)

## Category names

Rules for category names are as follows:

- must contain only lowercase characters, numbers, and hyphens
- must not start or end with a hyphen

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L57-L64), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L13-L20)

## Subcategory names

Rules for subcategory names are as follows:

- must contain only letters, numbers, spaces, commas, periods, parentheses, underscores, and hyphens

See: [iRODS rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/d9e8c8d0699f692e11eed8e8aa6c8fb136461af3/uuGroupPolicyChecks.r#L66-L75), [Python rule](https://github.com/UtrechtUniversity/yoda-ruleset/blob/e61f7e088c2f046d2fbe7b1095ff608f229d19ae/util/yoda_names.py#L23-L30)