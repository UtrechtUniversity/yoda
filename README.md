# yoda-ansible
[Ansible](https://docs.ansible.com) scripts for automatic deployment of Yoda:
a system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.

## Requirements
### Control machine requirements
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.6)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 5.2)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 2.2)

### Managed node requirements
* [CentOS](https://www.centos.org/) (>= 7.4)

## Deploying Yoda development instance
There are two example instances available for deployment
in the development environment.
Instance '[full](environments/development/full/)' deploys all functional roles to separate virtual machines.
Instance '[allinone](environments/development/allinone/)' deploys all functional roles to one virtual machine.
The guide below will deploy the 'allinone' instance with the default [configuration](CONFIGURATION.md).

Configure the virtual machines for development:
```bash
vagrant --instance=allinone up
```

On a Windows host first SSH into the Ansible controller virtual machine (skip this step on GNU/Linux or macOS):
```bash
vagrant ssh controller
cd ~/yoda-ansible
```

Deploy Yoda to development virtual machines:
```bash
ansible-playbook -i environments/development/allinone/ playbook.yml
```

Provision Yoda with test data:
```bash
ansible-playbook -i environments/development/allinone/ test.yml
```

Provision Yoda with zabbix agent and yoda monitoring scripts:
```bash
ansible-playbook -i environments/development/allinone/ zabbix.yml
```

Add following hosts to /etc/hosts (GNU/Linux or macOS) or  %SystemRoot%\System32\drivers\etc\hosts (Windows):
```
192.168.50.10 portal.yoda.test
192.168.50.10 data.yoda.test
192.168.50.10 public.data.yoda.test
192.168.50.10 public.yoda.test
192.168.50.10 eus.yoda.test
```

## Upgrading Yoda development instance
Upgrading the Yoda development instance to the latest version can be done by running the Ansible playbooks again.

On a Windows host first SSH into the Ansible controller virtual machine (skip this step on GNU/Linux or macOS):
```bash
vagrant ssh controller
cd ~/yoda-ansible
```

Upgrade Ansible scripts:
```bash
git pull
```

Upgrade Yoda instance:
```bash
ansible-playbook -i environments/development/allinone/ playbook.yml
```

## Documentation
* [design overview of the Ansible scripts](DESIGN.md).
* [configuration of Yoda](CONFIGURATION.md)
* [deployment of Yoda](DEPLOYMENT.md)

## License
This project is licensed under the GPL-v3 license.
The full license can be found in [LICENSE](LICENSE).
