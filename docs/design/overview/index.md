---
title: System Overview
parent: Software Design
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

[Technical design](research-space.md){: .btn }

### Vault space
The vault space implements a FAIR data publication workflow.

[Technical design](vault-space.md){: .btn }

### Statistics
The statistics module provides insight in research groups storage usage.

[Technical design](statistics.md){: .btn }

### Group manager
The group-manager is used to control access permissions of users based on group membership and the role inside a group.
It enables the distribution of access rights to data within Yoda with minimal aid of administrators.

[Technical design](group-manager.md){: .btn }

### User
The user module provides settings and notifications.

## Additional modules

### Intake
This module processes uploaded YOUth programme experiment data, and facilitate its archival in the vault by a data manager.

[Technical design](intake.md){: .btn }

### Datarequest
Module adding support for the submission, review and approval of requests to obtain research data stored in Yoda.

[Technical design](data-requests.md){: .btn }

### Deposit space
The deposit space implements a data deposit workflow to the vault space.

[Technical design](deposit-space.md){: .btn }

## Overview
![System overview](img/system-overview.png)
