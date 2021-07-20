---
title: System Overview
parent: Software design
nav_order: 1
has_children: true
has_toc: false
---
# System overview

Yoda is a research data management service that enables researchers and their partners to securely deposit, share, publish and preserve large amounts of research data during all stages of a research project.

Yoda consists of several core modules and has several additional modules providing additional functionality.

## Core modules

### Research space
The research space implements a data deposit workflow to the vault space.

[Technical design](/design/overview/research-space.html)

### Vault space
The vault space implements a FAIR data publication workflow.

[Technical design](/design/overview/vault-space.html)

### Statistics

[Technical design](/design/overview/statistics.html)

### Group manager
The group-manager is used to control access permissions of users based on group membership and the role inside a group.
It enables the distribution of access rights to data within Yoda with minimal aid of administrators.

[Technical design](/design/overview/group-manager.html)

### User


## Additional modules

### Intake

### Datarequest
Module adding support for the submission, review and approval of requests to obtain research data stored in Yoda.

[Technical design](/design/overview/data-requests.html)

### Deposit space
The deposit space implements a data deposit workflow to the vault space.

[Technical design](/design/overview/deposit-space.html)

## Overview
![System overview](img/system-overview.png)
