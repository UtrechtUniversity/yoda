# Asynchronous and Privileged Execution
Yoda uses delayed- and remote rule execution.
There are different reasons to apply these constructs, and different ways to use these.
Currently there is a bug in iRods whereby output parameters are not passed to delayed- or remote rules.
This document explains where and how these constructs are applied.

## Concerns
The following concerns need to be dealt with:
1. Security: we must protect the integrity/availability of data in the vault.
2. Interactivity: the interactive user should not wait for tasks.
3. Scalability: tasks with long execution time should not block other processes.
4. Tracability: it should be tracable who was responsible for certain changes.

To address thece concerns, we made the following decisions:

* **Decision: asynchronous execution of tasks with long- or uncertain execution time**.  Tasks that require long (say: more than 2 sec) or uncertain execution must be executed asynchronous from the interactive session.  
  **Rationale**: this allows the interactive session to continue (Concern 2), and these jobs to be scheduled/prioritized (Concern 3).  
  **Impact**: The interactive user is not informed of the result of the task, but that the task is pending. The user should be informed of the end-result via alternative channels.

* **Decision: exclusive privileges for vault**. Tasks in the vault require exclusive privileges. These privileges may only be assigned to actors that can be trusted.   
  **Rationale**: Data in the vault must be protected from undesired changes that may damage the integrity/authenticity that is required for reuse of the data (Concern 1).  
  **Impact**: Privileges may not be assigned to an interactive user, as credentials may be compromised and to prevent human errors. Privileges must be limited to defined procedures that can be trusted to maintain integrity/authenticity. The system must register who ordered such a procedure (Concern 4).

## Solutions

We identified the following constructs to provide privileged and/or asynchronous execution:

1.	ExecCmd-of-irule for privileged execution.
2.	Delayed Rule for asynchronous execution. Currently this does not work in all cases, due to a bug with for delayed rules with output parameters in the top-level call.
3.	Cronjob for asynchronous AND privileged execution. This allows a job to be 'picked up' and executed within the system environment. Drawback: asynchronous, cronjobs can only be scheduled at minute-granularity, so certain jobs require ~1m to start.  We use cronjobs as a fallback when we cannot use delayed rules due to a bug in irods.

The table below describes the ideal application of the above constructs. For now, the the cronjob is sometimes used for all async executions (bottom line).

| | **User Environment** | **System Environment** |
| --- | --- | --- |
| **Synchronous** | Default | Use ExecCmd |
| **ASynchronous** | Delayed Rule | Delayed Rule + ExecCmd |  


## Further Work

* Discuss the motivation for using the system/iRods user to increase privileges. Should we ideally use a specific user/role with specific privileges for the vault?  
* Discuss how the state model is reflected in the publication space.
* Discuss applying 'pending' states to the toVault as well, in line with the pending states for publication.
* Deletion of Data Package from the vault not yet implemented.
* Create state model for revisions and replications.
* Create state model for updating metadata.



# Appendix: Overview of rules and solutions

The image below shows the state model, and indicates the actions that require asynchronous execution and/or privileges. The table below described the individual actions.
![Actions in State Model](./img/ExecutionInStateModel.png)



| #  | Action | (a)sync | Context | State Change | Comment |
| -- | ------ | ------- | ------- | -------- | ------- |
| 1a | Research2Vault (request) | sync | user |  | Register Action and request execution |
| 1b | Research2Vault (execution) | **async** | **system** | ACCEPTED - SECURED<br/>New object: UNPUBLISHED | Copy files |
| 2a | Vault2Research (request) | sync | user |  | Register action and request execution |
| 2b | Vault2Research (execution) | **async** | user | New object: LOCKED | Copy files |
| 3a | SubmitPublication (request) | sync | user |  | Register action  and request execution |
| 3b | SubmitPublication (execution) | sync | **system** | UNPUBLISHED - SUBMITTED_FOR_PUBLICATION | |
| 4a | ApprovePublication (request) | sync | user | | Register action ande request execution |
| 4b | ApprovePublication (execution) | sync | **system** | SUBMITTED_FOR_PUBLICATION - APPROVED_FOR_PUBLICATION | trigger Publish |
| 5  | Publish | **async**| **system** |  APPROVED_FOR_PUBLICATION - PUBLISHED | Create/Register DOI, PMH, etc.<br/>*there is no registered within for public area?!* |
| 6a | RejectPublication (request) | sync | user | | Register action and request execution |
| 6b | RejectPublication (execution) | sync | **system** | SUBMITTED_FOR_PUBLICATION - UNPUBLISHED | *(is nog async, kan tzt sync worden)* |
| 7a | Published2pending (request) | sync | user |  | Register action and request execution |
| 7b | Published2pending (execute) | sync | **system** | PUBLISHED - PENDING_DEPUBLICATION  |   |
| 7c | Pending2depublished |**async** | **system** | PENDING_DEPUBLICATION - DEPUBLISHED | Update/register DOI, PMH, etc.|
| 8a | Republish2pending (requestt) | sync | user | | Register action and request execution |
| 8b | Republish2pending (execution) | sync | **system** | DEPUBLISHED - PENDING_REPUBLICATION | trigger pending2published |
| 8c | Pending2published | **async** | **system** | PENDING_REPUBLICATION - PUBLISHED |Update/register DOI, PMH, etc., |
| 9  | Revisioning | **async** | user |  | |
| 10 | Replication | **async** | user |  | |
| 11a | Update Vault Metadata (request) | sync | user |  | Register action and request execution |
| 11b | Update Vault Metadata (execution) | sync | **system** |  | Create metadata updates and trigger publication actions |
| 11c | Update Vault Metadata (publishing)| **async** | **system** | | Update/register DOI, PMH, etc.|

Note that all  actions that require async/system execution are preceded by a synchronous user action that registers the action, and triggers the async/system action: 1, 2, 3, 4, , 6, 7, 8. **Overweeg deze regels weg te laten!**

Actions are registered(in principle) in iCat, in provenance (user actions) and in system log.
Registration in system log not always consequently...
