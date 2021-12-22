---
parent: Administration Tasks
title: Configuring Data Access Passwords
nav_order: 13
---
# Configuring Data Access Passwords
Instruction on how to configure Data Access Passwords.

## Configuring the variables
When creating a new Yoda instance, setup the variables in the group_vars as explained in [Configuring Yoda](configuring-yoda.md) and run the playbook.
Alternatively, you can choose to pass the variables with the *--extra-vars* option every time when running the Ansible playbook.
The development group_vars contains examples for all of the variables.

For Data Access Passwords to function properly it requires the following variables to be set:
- enable_tokens (default: `false`), used by Ansible during setup.

For customization purposes, you can also configure:
- token_database
- token_length
- token_lifetime
