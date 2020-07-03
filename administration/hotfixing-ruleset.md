# Applying a local change to a ruleset

If a local change (hotfix) to a ruleset is needed, the following method is recommended:

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
