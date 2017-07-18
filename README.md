yoda-ansible
============
Ansible scripts for automatic deployment of YoDa: a system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.

Requirements
------------
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.3)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 5.1)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 1.9)

Usage
-----
```bash
vagrant up
ansible-playbook playbook.yml
```

License
-------
This project is licensed under the GPL-v3 licence
The full license can be found in [LICENSE](LICENSE).
