# yoda-ansible
[Ansible](https://docs.ansible.com) scripts for automatic deployment of Yoda:
a system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.

## Requirements
### Control machine requirements
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.4)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 5.1)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 1.9)

### Managed node requirements
* [CentOS](https://www.centos.org/) (>= 7.3)

## Deploying Yoda development instance
There are two example instances available for deployment
in the development [environment](environments/development/).
Instance 'full' deploys all functional roles to separate virtual machines.
Instance 'allinone' deploys all functional roles to one virtual machine.
The guide below will deploy the 'allinone' instance with the default [configuration](CONFIGURATION.md).

### GNU/Linux or macOS host
Configure the virtual machines for development:
```bash
vagrant --instance=allinone up
```

Deploy Yoda to development virtual machines:
```bash
ansible-playbook playbook.yml --limit=allinone
```

Provision Yoda with test data:
```bash
ansible-playbook test.yml --limit=allinone
```

Add following hosts to /etc/hosts:
```
192.168.50.10 portal.yoda.dev
192.168.50.10 data.yoda.dev
192.168.50.10 moai.yoda.dev
192.168.50.10 public.yoda.dev
```

### Windows host
Configure the virtual machines for development:
```bash
vagrant --instance=allinone up
```

SSH to Ansible controller virtual machine:
```bash
vagrant ssh controller
cd ~/yoda-ansible
```

Deploy Yoda to development virtual machines:
```bash
ansible-playbook playbook.yml --limit=allinone
```

Provision YoDa with test data:
```bash
ansible-playbook test.yml --limit=allinone
```

Add following hosts to %SystemRoot%\System32\drivers\etc\hosts:
```
192.168.50.10 portal.yoda.dev
192.168.50.10 data.yoda.dev
192.168.50.10 moai.yoda.dev
```

## Upgrading Yoda development instance
Upgrading the Yoda development instance to the latest version can be done by running the Ansible playbooks again.

### GNU/Linux or macOS host
Upgrade Ansible scripts:
```bash
git pull
```

Upgrade YoDa instance:
```bash
ansible-playbook playbook.yml --limit=allinone
```

### Windows host
SSH to Ansible controller virtual machine:
```bash
vagrant ssh controller
cd ~/yoda-ansible
```

Upgrade Ansible scripts:
```bash
git pull
```

Upgrade YoDa instance:
```bash
ansible-playbook playbook.yml --limit=allinone
```

## Documentation
* [design overview of the Ansible scripts](DESIGN.md).
* [configuration of Yoda](CONFIGURATION.md)
* [deployment of Yoda](DEPLOYMENT.md)

## License
This project is licensed under the GPL-v3 license.
The full license can be found in [LICENSE](LICENSE).
