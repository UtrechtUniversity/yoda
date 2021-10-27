# Yoda  [![Release](https://img.shields.io/github/v/tag/UtrechtUniversity/yoda?sort=semver)](https://github.com/UtrechtUniversity/yoda/releases) [![License](https://img.shields.io/github/license/UtrechtUniversity/yoda.svg?maxAge=2592000)](/LICENSE)

A system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.

## What is this?
Yoda is a research data management solution developed by Utrecht University and used by multiple institutes around the world.
It enables researchers and their partners to securely deposit, share, publish and preserve large amounts of research data during all stages of a research project.

This repository is the staring point for using Yoda and contains the [Ansible](https://docs.ansible.com) scripts for automatic deployment of Yoda.

## Requirements
### Control machine requirements
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.9)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 6.x)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 2.2.x)

### Managed node requirements
* [CentOS](https://www.centos.org/) (>= 7.4)

## Documentation
Documentation is hosted on: https://utrechtuniversity.github.io/yoda/

## Contributing
### Code
Instructions on how to setup your development environment and other useful instructions for development can be found in the [documentation](https://utrechtuniversity.github.io/yoda/development/setting-up-development-environment.html).

### Bug reports
We use GitHub for bug tracking.
Please search existing [issues](https://github.com/UtrechtUniversity/yoda/issues) and create a new one if the issue is not yet tracked.

## License
This project is licensed under the GPL-v3 license.
The full license can be found in [LICENSE](LICENSE).
