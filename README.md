yoda-ansible
============
Ansible scripts for automatic deployment of YoDa: a system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.

Requirements
------------
### Control machine requirements
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.3)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 5.1)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 1.9)

### Managed node requirements
* CentOS 7.3

Usage
-----
### GNU/Linux or macOS host
Configure the virtual machines for development:
```bash
vagrant up
chmod 0600 vagrant/ssh/vagrant
```

Deploy YoDa to development virtual machines:
```bash
ansible-playbook playbook.yml
```

### Windows host
Configure the virtual machines for development:
```bash
vagrant up
```

Deploy YoDa to development virtual machines:
```
vagrant provision controller
```

License
-------
This project is licensed under the GPL-v3 licence
The full license can be found in [LICENSE](LICENSE).
