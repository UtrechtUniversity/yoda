---
grand_parent: Software Design
parent: Processes
---
# To vault process in research module

This document does not fully describe the process to push datapackages to the vault. Only the
technical choices made to implement the process are described here. The process is described
in the architectural state model.

## Folder status
Each folder in the research area is initialized without any status information. This is regarded as the folder status *Folder*. Every other status is defined
by the metadata field *org_status* on the collection. The valid statuses and transitions are defined in iiConstant like below.

```
# \brief All research folder states.
FOLDER = "";
LOCKED = "LOCKED";
SUBMITTED = "SUBMITTED";
ACCEPTED = "ACCEPTED";
REJECTED = "REJECTED";
SECURED = "SECURED";

# \constant IIFOLDERTRANSITIONS
IIFOLDERTRANSITIONS = list((FOLDER, LOCKED),
			   (FOLDER, SUBMITTED),
			   (LOCKED, FOLDER),
			   (LOCKED, SUBMITTED),
			   (SUBMITTED, FOLDER),
			   (SUBMITTED, ACCEPTED),
			   (SUBMITTED, REJECTED),
			   (REJECTED, LOCKED),
			   (REJECTED, FOLDER),
			   (REJECTED, SUBMITTED),
			   (ACCEPTED, SECURED),
			   (SECURED, LOCKED),
			   (SECURED, FOLDER),
			   (SECURED, SUBMITTED))
```

## Status Policies
All the status transitions are handled by rules in *iiFolderStatusTransistions.r*. Basically they set the org_status of the folder to the new status and
PEP's in *iiPolicies.r* will check if the transition is legal and call pre and post procedures for each transition. The checks if a status transition is
allowed are found in *iiPolicyChecks.r*.

The pre and post conditions are run based on the manipulation of the *org_status* metadata. This means every status transition can be triggered with the
*imeta* command. Illegal transitions will be blocked with *msiOprDisallowed*.

## Datamanager approval
When a datamanager is present, a datapackage submitted to the vault by a researcher will remain in the submitted state. The datamanager can approve or reject
the package for further processing. A researcher also has the opportunity to unsubmit the package. Because a datamanager only has read access to the research
area, he/she cannot edit the *org_status* directly. To work around this issue the sudo microservices are used to temporarily enable the datamanager to set the
*org_status* to 'ACCEPTED' or 'REJECTED'. The rules can be found in *iiDatamanagerPolicies.r* and *iiSudoPolicies.r*.

A research group without a datamanager can submit packages to the vault directly. Any submitted folder will be transitioned to 'ACCEPTED' state immediately after
submission.

## Copy to vault
The **copy-accepted-folders-to-vault.r** cronjob in the tools directory of the research ruleset will copy any folder in 'ACCEPTED' state to the vault and set it to
'SECURED' state when successful. The copy uses `irsync` starting from the the 'ACCEPTED' folder. The metadata will be copied as well. The **retry-copy-to-vault.r** cronjob follows the same process, only with folders that have previously failed to copy and thus have a 'RETRY' status.

## Research vault
For each research group a vault group with a vault collection is created. Only the rodsadmin will be a member. This folder is read-only for managers
and normal users of the research group. When a datamanager group for the category is present it will get read-only access as well. Inheritance is
switched off. This makes it possible to manage permissions for each vault package separately. A datamanager gets control over it.

## Granting and revoking read access to the vault for the research group
The datamanager is allowed to use the sudo microservice msiSudoObjAclSet to grant and revoke read access to packages in the vault. This is configured in
*iiSudoPolicies.r* and *iiDatamanagerPolicies.r* to not interfere with existing sudo policies in the yoda-ruleset. The only action the datamanager is
allowed to do is set permissions starting from the root of a vault package to read for the research group with the same basename as the vault.

## No datamanager
When there is no datamanager present the permissions can only be managed by the rodsadmin. Read-only for the research group by default could be implemented.
