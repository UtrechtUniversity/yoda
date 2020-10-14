# Development tips
A collection of tips to make Yoda development easier.

Watch latest iRODS log without unnecessary noise:
```bash
ls -t /var/lib/irods/log/rodsLog* | head -n1 | xargs -n 1 -- tail -f | grep -v "Agent process started for puser=rods"
```

Run flake8 checks on source file change (requires the `entr` package):
```bash
ls *py | entr flake8 *.py avu_json/*.py util/*.py --exclude=__init__.py --statistics```

Rebuild JS assets on source file change:
```bash
./node_modules/.bin/webpack -d -w```

Remove all existing data requests (to declutter your _development_ environment ;):
```bash
icd ../datarequests-research && ils | grep \ \  | sed 's/\ \ C-\ //' | xargs -I COLLPATH sh -c "ichmod -M -r own rods COLLPATH && irm -r COLLPATH"```
