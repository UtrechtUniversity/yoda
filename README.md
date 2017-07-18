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

Documentation
-------------

The main [playbook](playbook.yml) consists of four tiers:
* portal
* database
* iCAT
* resource

### portal tier
The portal tier provisions the host with the following:
* Apache webserver
* PHP
* iRODS iCommands & runtime
* YoDa portal and davrods

### database tier
The portal tier provisions the host with the following:
* PostgreSQL database
* iRODS database plugin

### iCAT tier
The portal tier provisions the host with the following:
* iRODS iCAT server & runtime
* iRODS microservices
* YoDa rulesets

### resource tier
The portal tier provisions the host with the following:
* iRODS resource server & runtime
* iRODS microservices
* YoDa rulesets

License
-------
This project is licensed under the GPL-v3 licence
The full license can be found in [LICENSE](LICENSE).
