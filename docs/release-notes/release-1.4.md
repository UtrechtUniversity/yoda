# Release notes Yoda version 1.4 (December 2018)

Version: 1.4

Released: December 2018

## New features since Yoda version 1.3
- Support for external users through the External User Service
- Data package access rights published to DataCite and OAI-PMH
- Performance improvements for the Intake module. Note: if a study shows unscanned files, please scan again.
- UX improvements to the login form
- Several performance and security improvements

## Upgrading from Yoda version 1.3
Upgrade is supported by Ansible (2.7.x). No migrations required.

Add the following fields to the Ansible environment files
(see [yoda-ansible/CONFIGURATION.md](https://github.com/UtrechtUniversity/yoda-ansible/blob/development/CONFIGURATION.md) for description):
- yoda_eus_fqdn
- epic_key
- epic_cert
- eus_api_fqdn
- eus_api_secret
- eus_db_password
- eus_smtp_host
- eus_smtp_port
- eus_smtp_user
- eus_smtp_password
- eus_smtp_from_address
- eus_smtp_replyto_address
- eus_mail_template
- repo_only (optional)
