---
grand_parent: Software Design
parent: System Overview
nav_order: 8
---
# Intake module

## Introduction

This page describes the specifications of the Yoda intake module. The main purpose of this module
is to process uploaded YOUth programme experiment data, and facilitate its archival in the vault by a data manager.

Experiment data would first be uploaded into an intake
folder by a lab assistant or other employee ("intaker"). The intake module has a scan function the
data manager can use to extract dataset information from file and folder names so that data can be grouped
by dataset. Finally, the data manager can use the intake module to lock datasets in the Yoda vault.

The rest of this page contains specifications of the expected data object and collection names.

## Data object and collection name specifications

### Allowed characters

Data object names (file names) and collection names (folder names) should consist of only these characters:
- Letters, either upper case or lower case (Latin alphabet: a-z, A-Z)
- Digits: 0-9
- Underscores (\_)
- Hyphens (-)
- Dots (.)

### WEPV data in names

Datasets are identified by WEPV properties (Wave, Experiment, Pseudo code, Version) which are derived from data object
and/or collection names.  The wave, experiment and pseudo code elements are compulsory. The version element is optional,
and has a default value of "Raw". Either underscores ("\_") or hyphens ("-") can be used as separators between WEPV
elements in data object or collection names. WEPV elements may be defined at different levels in the tree.

WEPV elements in a path are processed from left to right. The first folder which has complete WEPV data (i.e. wave, experiment and
pseudo code are present in the path of the folder, including its parent folders) is considered to be the
root folder of the dataset. If only the data object itself has complete WEPV data, the data object itself is considered
to be the root of the dataset.

Here is an example of a data object in a dataset:

    Y:/grp-vault-youth/malu/20w/echo/Y2015M05/D27/20w_B54321/I0000000.vol
                                                  ^^^^^^^^^^

In this example, the experiment type element ("echo") is defined at a different level from the wave ("20w") and
pseudo ID ("B54321") element. The folder indicated by the carets is considered to be the root folder of the dataset,
since it is the topmost folder with complete WEPV element data.

#### Wave values

Waves before birth have a "w" (week) suffix, whereas waves after birth have a month ("m") or year ("y") suffix.

The 9y, 12y and 15y waves are part of the adolescent cohort, whereas the other waves are part of the baby / child cohort.

Valid waves are:
- 20w
- 30w
- 0m
- 5m
- 10m
- 3y
- 6y
- 9y
- 12y
- 15y

#### Experiment type values

Valid experiment types are:

- pci
- echo
- faceemo
- coherence
- infprogap
- infsgaze
- infpop
- chprogap
- chantigap
- chsgaze
- pciconflict
- pcivacation
- peabody
- discount
- cyberball
- trustgame
- other
- inhibmockbehav
- inhibmribehav
- emotionmribehav
- emotionmriscan
- anatomymriscan
- restingstatemriscan
- dtiamriscan
- dtipmriscan
- mriqcreport
- mriqceval
- vasmri
- vasmock
- looklisten
- handgame
- infpeabody
- delaygratification
- dtimriscan
- inhibmriscan
- chdualet
- functionalmriscan
- infdualet

The "other" type is used for questionnaires, logs and unknown types of data.

#### Pseudo code format

Pseudo codes consist of a letter "a" (adolescent), "b" (baby) or "p" (adolescent pilot) followed
by five digits.

#### Version format

Version elements consist of "ver", followed by a version name. The version element is optional, and
defaults to a version named "Raw". The version name must begin with an upper case letter. The
version name must consist of only alphanumeric characters.

Examples:
- verRaw
- verVersionName

## Acknowledgements and provenance

This page is based on the original specification document titled _Yoda &mdash; Youth Cohort Data Intake Specificaties_,
by Jonas Sweep, Chris Smeele and Ton Smeele, version 0.12. Information regarding quality criteria specific to experiment
types has not been copied from the original document, since quality checks specific to experiment types have been removed
from the intake module.
