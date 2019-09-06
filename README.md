# Yoda [![Release](https://img.shields.io/github/v/tag/UtrechtUniversity/yoda-ansible?sort=semver)](https://github.com/UtrechtUniversity/yoda-ansible/releases)[![License](https://img.shields.io/github/license/UtrechtUniversity/yoda-ansible.svg?maxAge=2592000)](/LICENSE)

A system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.

## What is this?
Yoda is a research data management solution developed by Utrecht University and used by multiple institutes around the world.
It provides researchers and their partners with a workspace and an archive that enables them to collaborate, deposit, publish and preserve research data.

This repository is the staring point for using Yoda and contains the [Ansible](https://docs.ansible.com) scripts for automatic deployment of Yoda.


## Requirements
### Control machine requirements
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.7)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 6.x)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 2.2.x)

### Managed node requirements
* [CentOS](https://www.centos.org/) (>= 7.4)

## Documentation
Documentation is hosted on: https://utrechtuniversity.github.io/yoda-docs/

## License
This project is licensed under the GPL-v3 license.
The full license can be found in [LICENSE](LICENSE).
