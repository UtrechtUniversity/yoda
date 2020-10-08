# Development tips
A collection of tips to make Yoda development easier.

Watch latest iRODS log without unnecessary noise:
```bash
ls -t /var/lib/irods/log/rodsLog* | head -n1 | xargs -n 1 -- tail -f | grep -v "Agent process started for puser=rods"
```
