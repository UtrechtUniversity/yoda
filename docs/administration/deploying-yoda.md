---
parent: Administration Tasks
title: Deploying Yoda
nav_order: 1
---
# Deploying Yoda
Instructions needed for deploying a (new) Yoda instance.

## Deploying new instance
[Configure](configuring-yoda.md) the new instance and run the Yoda playbook to deploy.
For example, deploying the instance 'yoda' in an environment called 'production':
```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i environments/development playbook.yml --limit=yoda -K
```

## Upgrading existing instance
To upgrade an existing Yoda instance update your Yoda Ansible repository to include the latest changes:
```bash
git pull
```

Install all Ansible collections needed to deploy Yoda:
```bash
ansible-galaxy collection install -r requirements.yml
```

Upgrade the [configuration](configuring-yoda.md) of the Yoda Instance and then run the Yoda playbook:
```bash
ansible-playbook -i environments/development/allinone playbook.yml --limit=yoda -K
```

You may want to run the Yoda playbook in check mode first to see the changes it will make:
```bash
ansible-playbook -i environments/development/allinone playbook.yml --limit=yoda -CDK
```
