# yoda-ansible
Ansible scripts for automatic deployment of YoDa: a system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.

## Requirements
### Control machine requirements
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.3)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 5.1)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 1.9)

### Managed node requirements
* [CentOS](https://www.centos.org/) (>= 7.3)

## Usage
There are two example instances available for deployment
in the development [environment](environments/development/).
Instance 'full' deploys all functional roles to separate virtual machines.
Instance 'allinone' deploys all functional roles to one virtual machine.

### GNU/Linux or macOS host
Configure the virtual machines for development:
```bash
vagrant --instance=allinone up
```

Deploy YoDa to development virtual machines:
```bash
ansible-playbook playbook.yml --limit=allinone
```

Provision YoDa with test data:
```bash
ansible-playbook test.yml --limit=allinone
```

Add following hosts to /etc/hosts:
```
192.168.50.10 portal.yoda.dev
192.168.50.10 data.yoda.dev
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

Deploy YoDa to development virtual machines:
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
```

## License
This project is licensed under the GPL-v3 license.
The full license can be found in [LICENSE](LICENSE).
