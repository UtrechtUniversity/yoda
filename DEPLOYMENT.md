# Deployment
Instructions needed for deploying a (new) Yoda instance.

## Deploying new instance
[Configure](CONFIGURATION.md) the new instance and run the Yoda playbook to deploy.
For example, deploying the instance 'yoda' in an environment called 'production':
```bash
ansible-playbook -i environments/development playbook.yml --limit=yoda -K
```

## Upgrading existing instance
To upgrade an existing Yoda instance update your Yoda Ansible repository to include the latest changes:
```bash
git pull
```

Then run the Yoda playbook:
```bash
ansible-playbook -i environments/development playbook.yml --limit=yoda -K
```

You may want to run the Yoda playbook in check mode first to see the changes it will make:
```bash
ansible-playbook -i environments/development playbook.yml --limit=yoda -CDK
```
