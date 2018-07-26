# Release notes Yoda version 1.3 (to be released)

## New features since Yoda version 1.2
- Upgrade from iRODS 4.1.11 to 4.2.3
-

## Upgrading from 1.2
Upgrade is supported by Ansible. No migrations required.
Add the following fields to the Ansible environment files
(see [yoda-ansible/CONFIGURATION.md](https://github.com/UtrechtUniversity/yoda-ansible/blob/development/CONFIGURATION.md) for description):
- credential_files
- send_notifications
- notifications_sender_email
- notifications_reply_to
- smtp_server
- smtp_username
- smtp_password
- epic_url
- epic_handle_prefix

## Known Issues
- Ordering of data in tables is not working. Clicking column sort headers have been disabled and are not shown.
