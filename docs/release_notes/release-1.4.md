# Release notes Yoda version 1.4

## New features since Yoda version 1.3
- Support for external users through the External User Service
- Data package access right published to DataCite and OAI-PMH
- UX improvements to the login form
- Several performance and security improvements

## Upgrading from Yoda version 1.3
Upgrade is supported by Ansible. No migrations required.
Add the following fields to the Ansible environment files
(see [yoda-ansible/CONFIGURATION.md](https://github.com/UtrechtUniversity/yoda-ansible/blob/development/CONFIGURATION.md) for description):
- yoda_eus_fqdn
- eus_api_secret
