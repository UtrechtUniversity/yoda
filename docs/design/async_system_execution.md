# Asynchronous and Privileged Execution
YODA uses delayed- and remote rule execution. There are different reasons to apply these constructs, and different ways to use these. Currently there is a bug in iRods whereby output parameters are not passed to delayed- or remote rules. This document analyses / decides how to apply these constructs.

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

(@Felix, can you describe these in more detail?)

1.	PHP Call ‘change state to x’, triggering an ExecCmd
2.	Cronjob. This allows a job to be 'picked up' and executed within the system environment. Drawback: cronjobs can only be scheduled at minute-granularity, so certain jobs require ~1m to start, which implies asynchrounous execution. Requires Mutex to ensure that jobs are not picked up twice.
3.	Delayed Rule. Bug: output-params.

De decided to apply the following:

* **Decision: Apply delayed rule and ExecCmd for resp. asynchronous and system execution**. The delayed rule is applied for executing tasks with (possibly) long execution time 
  in asynchronously, and ExecCmd is applied to have the (privileged/non-interactive) system user perform write action in the vault. Tasks that require vault privileges and asynchronous execution apply both the delayed rule and ExecCmd.  
  **Rationale**:   
  **Impact**:  
  
  
| | **User Environment** | **System Environment** |
| --- | --- | --- |
| **Synchronous** | Default | Use ExecCmd |
| **ASynchronous** | Delayed Rule | Delayed Rule + ExecCmd |  
  

# Appendix: Overview of rules and solutions

The image below shows the state model, and indicates the actions that require asynchronous execution and/or privileges. The table below described the individual actions.
![Actions in State Model](./img/ExecutionInStateModel.png)

Notes, Questions, etc:
* Deletion of a data package (unpublished/depublished should require privileges?!
* Revisioning, Replication and updating metadata were not part of the state model (yet).
* Vault2Research implies adding a new transition from begin to locked in the research state model.
* 1a: Compare to publishing the actual publishing is connected to the approval.
* 1b: should add ExecCmd for system execyion?
* Registration of actions: where is this registered? Provenance, Log? What are the action-names?
* To what extent do we / should we maintain stated in the publication space?
* Is it desirable to use the system environment for execution vault actions, or should we create a dedicated "Vault/Archivist"-role+environment?
* 7c and 8c: these constructs use/need output params? Is this the current situation? 


| #  | Action | (a)sync | Context | Solution | Comment |
| -- | ------ | ------- | ------- | -------- | ------- |
| 1a | Research2Vault (request) | sync | user | *normal* execution | 1. Register action (Accept),<br/>2. request execution |
| 1b | Research2Vault (execution) | **async** | **system** | Delayed (no output params) | 1. Copy files,<br/>2. update research state (secured) and<br/> 3. update vault state (unpublished) | 
| 2a | Vault2Research (request) | sync | user | *normal* execution | 1. Register action (*???*),<br/>2. request execution |
| 2b | Vault2Research (execution) | **async** | user | Delayed (no output params) | 1. Copy files,<br/>2. update research state (locked) | 
| 3a | SubmitPublication (request) | sync | user |  *normal* execution | 1. Register action (*???*),<br/>2. request execution |
| 3b | SubmitPublication (execution) | sync | **system** | ExecCmd | 1. Update vault state (submitted for publication)|
| 4a | ApprovePublication (request) | sync | user | *normal* execution | 1. Register action (*???*),<br/>2. request execution |
| 4b | ApprovePublication (execution) | sync | **system** | ExecCmd | 1. Update vault state (submitted for publication), <br/>2. trigger Publish |
| 5  | Publish | **asyn**| **system** | Delayed  (no output params) + ExecCmd *temporarily:cronjob* | 1. Create/Register DOI, PMH, etc.<br/>2. update vault state (published)<br/>*there is no registered within for public area?!* |
| 6a | RejectPublication (request) | sync | user | *normal* execution | 1. Register action (*???*),<br/>2. request execution |
| 6b | RejectPublication (execution) | sync | **system++ | ExecCmd | 1. Update vault state (unpublished) *(is nog async, kan tzt sync worden)* |
| 7a | Published2pending (request) | sync | user | *normal* execution | 1. Register action (*???*),<br/>2. request execution |
| 7b | Published2pending (execute) | sync | **system** | ExecCmd | 1. Update vault state (depublish-pending), <br/>2. trigger pending2published |
| 7c | Pending2depublished |**async** | **system** | Delayed rule **with** output params + ExecCmd | *temporarily a cronjob*<br/>1. Update/register DOI, PMH, etc.,<br/>2. update vault state (depublished) |
| 8a | Republish2pending (requestt) | sync | user | *normal* execution | 1. Register action (*???*),<br/> 2. request execution |
| 8b | Republish2pending (execution) | sync | **system** | ExecCmd | 1. update vault state (republish-pending),<br/>2. trigger pending2published |
| 8c | Pending2published | **async** | **system** | Delayed **with** output params + ExecCmd | *temp solution: cronjob*<br/>1. Update/register DOI, PMH, etc.,<br/>2. update vault state (published) |
| 9  | Revisioning | **async** | user | Delayed (no out-params) | *@Felix?* |
| 10 | Replication | **async** | user | Delayed (no out-params) | *@Felix* |
| 11a | Update Vault Metadata (request) | sync | user | *normal* execution | 1. Register action,<br/> 2. request execution |
| 11b | Update Vault Metadata (execution) | sync | **system** | ExecCmd | 1. Create metadata updates, <br/> 2. Trigger publication actions |
| 11c | Update Vault Metadata (publishing)| **async** | **system** | Delayed (no out-params) + ExecCmd | *temp solution: cronjob, for consistency with publish solution*<br/> 1. Update/register DOI, PMH, etc.|
