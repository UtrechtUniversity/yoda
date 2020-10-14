# Development tips
A collection of tips to make Yoda development easier.

Watch latest iRODS log without unnecessary noise:
```bash
ls -t /var/lib/irods/log/rodsLog* | head -n1 | xargs -n 1 -- tail -f | grep -v "Agent process started for puser=rods"
```

Run flake8 checks on source file change (requires the `entr` package):
```bash
ls *py | entr flake8 *.py avu_json/*.py util/*.py --exclude=__init__.py --statistics```
