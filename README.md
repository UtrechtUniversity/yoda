<br/>
<p align="center">
  <a href="https://github.com/UtrechtUniversity/yoda">
    <img src="yoda.svg" alt="Yoda logo" width="652" height="212">
  </a>

  <p align="center">
    A system for reliable, long-term storing and archiving large amounts of research data during all stages of a study.
    <br/>
    <br/>
    <a href="https://utrechtuniversity.github.io/yoda/"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/UtrechtUniversity/yoda/issues/new?assignees=&labels=bug+%3Abug%3A&template=bug_report.md&title=%5BBUG%5D">Report Bug</a>
    .
    <a href="https://github.com/UtrechtUniversity/yoda/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFEATURE%5D">Request Feature</a>
    .
    <a href="https://github.com/UtrechtUniversity/yoda/discussions/categories/ideas">Share an idea</a>
    .
    <a href="https://github.com/UtrechtUniversity/yoda/discussions/categories/q-a">Ask a question</a>
  </p>
</p>

[![Release](https://img.shields.io/github/v/tag/UtrechtUniversity/yoda?sort=semver)](https://github.com/UtrechtUniversity/yoda/releases) [![License](https://img.shields.io/github/license/UtrechtUniversity/yoda.svg?maxAge=2592000)](/LICENSE)

## About the project
Yoda is a research data management solution developed by [Utrecht University](https://www.uu.nl/) and used by multiple institutes around the world.
It enables researchers and their partners to securely deposit, share, publish and preserve large amounts of research data during all stages of a research project.

This is the main repository of Yoda. It contains the [Ansible](https://docs.ansible.com) playbook for automated deployment, as well as the [documentation](https://utrechtuniversity.github.io/yoda/).

## Requirements
### Control machine requirements
* [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html) (>= 2.11.x)
* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) or [libvirt](https://libvirt.org/)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 2.3.x)

### Managed node requirements
* [CentOS](https://www.centos.org/) 7.x (>= 7.4). See also the [supported distribution list](docs/administration/supported-distributions.md)

## Documentation
Documentation is hosted on: https://utrechtuniversity.github.io/yoda/

## Contributing
### Code
Instructions on how to setup your development environment and other useful instructions for development can be found in the [documentation](https://utrechtuniversity.github.io/yoda/development/setting-up-development-environment.html).

### Bug reports
We use GitHub for bug tracking.
Please search existing [issues](https://github.com/UtrechtUniversity/yoda/issues) and create a new one if the issue is not yet tracked.

### Questions and ideas
The best place to reach us about questions and ideas regarding Yoda is on our [GitHub Discussions page](https://github.com/utrechtuniversity/yoda/discussions).

## License
This project is licensed under the GPL-v3 license.
The full license can be found in [LICENSE](LICENSE).
