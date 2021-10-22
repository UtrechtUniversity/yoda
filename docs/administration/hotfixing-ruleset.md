---
parent: Administration Tasks
title: Hotfixing ruleset
nav_order: 2
---
# Applying a local change to a ruleset

This page describes a method for making a temporary local change (hotfix) to a ruleset. Such a
hotfix can be used temporarily for testing. If the change is to be kept permanently, it is advisable
to [deploy the change using Ansible](local-ruleset-patch.md).

The commands below can be executed using the iRODS service account.

1. First clone another copy of the ruleset:
```bash
cd /etc/irods
git clone https://github.com/UtrechtUniversity/irods-ruleset-uu.git hotfix
```

2. Make changes to the ruleset (for example, meta.py) and compile the ruleset:
```bash
cd hotfix
vim meta.py
make install
```

3. Change the symlink to the fixed ruleset:
```bash
cd /etc/irods
ln -sfn hotfix rules_uu
```

If the change does not have the desired result, revert to the old ruleset by changing the symlink back and compiling the ruleset:
```bash
cd /etc/irods
ln -sfn irods-ruleset-uu rules_uu
cd irods-ruleset-uu
make install
```
