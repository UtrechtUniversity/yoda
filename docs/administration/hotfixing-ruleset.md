# Hotfixing ruleset
If in some case a hotfix on a rulset is needed, the following method is recommended:

First clone another copy of the ruleset:
```bash
cd /etc/irods
git clone https://github.com/UtrechtUniversity/irods-ruleset-uu.git hotfix
```

Make changes to the ruleset (for example, meta.py) and compile the ruleset:
```bash
cd hotfix
vim meta.py
make install
```

Change the symlink to the fixed ruleset:
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
