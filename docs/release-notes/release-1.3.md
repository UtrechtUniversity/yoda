# Release notes Yoda version 1.3 (November 2018)

Version: 1.3

Released: November 2018

## What's new in Yoda version 1.3
### Features
- Upgrade from iRODS 4.1.11 to 4.2.4
- Persistent identifier (EPIC-PID) for vault packages
- Data folder is now unlocked after securing it in in the vault
- CSV export in Statistics module for Yoda admin
- Data classification for groups added to the Group Manager
- Usability improvements in the Group Manager
- DataCite format support for the OAI-PMH service
- Email notifications when a package is published
- Several performance and security improvements

## Upgrading from Yoda version 1.2
Upgrade is supported by Ansible (2.7.x). No migrations required.

Make sure the delayed rule queue is empty before upgrading (`iqstat -a`).
Add the following fields to the Ansible environment files
(see [yoda/CONFIGURATION.md](https://github.com/UtrechtUniversity/yoda/blob/release-1.4/CONFIGURATION.md) for description):
- yoda_environment (replaces codeigniter_environment)
- credential_files
- send_notifications
- notifications_sender_email
- notifications_reply_to
- smtp_server
- smtp_username
- smtp_password
- epic_url
- epic_handle_prefix
