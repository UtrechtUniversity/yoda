---
grand_parent: Software Design
parent: System Overview
nav_order: 9
---
# Data requests module

## Introduction
This technical design document describes an approach to implementing support for
the submission, review and approval of requests to obtain research data stored
in Yoda.

## Definitions
- **Research group** A group of researchers belonging to a particular research
lab or otherwise collaborating on a common research goal. E.g. the Brain
Morphology Lab.

## Functional description
The supported workflows are described in this section. A sequence diagram
mapping the workflow is shown below.

![Workflow sequence diagram](img/datarequest/datarequest_workflow_sequence_diagram.png)

### Submission of data requests
A researcher seeking to obtain research data stored in Yoda must be able to
submit a request for this data.

A researcher may submit two kinds of data request:
- data requests made for the purpose of publishing the analysis results
- data requests for data assessment only (DAO; e.g. project-internal quality
  assurance)

In the first case, a research proposal must be submitted along with the data
request. The research proposal must describe the purpose for which the
researcher wants to obtain the requested data. No research proposal is submitted
along with a DAO data request.

In the subsequent sections, the workflows for the processing of a data request
for the purpose of publishing the analysis results will be described. DAO data
requests are treated in a separate section.

### Management and review of data requests
A project manager of a research group to which a data request is submitted must
be able to perform a cursory preliminary review of this data request, choosing
whether the request is accepted for further review, rejected with the
possibility of resubmission, or rejected with no possibility of resubmission.

Likewise, a data manager assigned as a custodian of data requested in a data
request must be also able to submit a review of this data request, indicating as
a recommendation to the project manager whether the data request should be
accepted for further review, rejected with the possibility of resubmission, or
rejected with no possibility of resubmission.

After a positive preliminary review and after review the data manager's
recommendation, a project manager must be able to assign a data request for
review to one or more members of a Data Access Committee (DAC), or to reject the
data request (either with or without the possibility of resubmission).

If a data request is assigned for review to the DAC, the project manager must be
able to set the length of the review period.

The DAC members must be able to review research proposals assigned to them, but
only within the review period set by the project manager.

### Final evaluation of data requests
A project manager must be able to give a final evaluation of a research proposal
based on the reviews by the data manager and the DAC member(s), therein
approving or rejecting the data request (either with or without the possibility
of resubmission).

### Preregistration of research proposals
After final approval of a data request by the project manager, the research
proposal of the data request must be preregistered by the researcher in the
research group's preregistry on the Open Science Framework.

The project manager must be able to confirm that the research proposal is
properly preregistered in the research group's preregistry on the Open Science
Framework.

### Creation of data transfer agreements (DTAs)
Once a data request and its accompanying research proposal have been approved,
the data manager must be able to create a DTA specifying the terms and
conditions under which the requested data is made available to the requesting
researcher.

### Approval of DTAs
Once a DTA has been created, the requesting researcher must be able to view the
DTA and register his agreement to the terms and conditions specified therein.

### Release of requested data
After the DTA has been signed by the requesting researcher, the data manager
may release the requested data to him. The means by which the data is
transferred to the researcher is outside of the scope of the data request
module.

## Technical description
To keep the complexity of the module to a minimum, existing Yoda functionality
and modules are used to implement the functional requirements.

### Submission of data requests
To allow anyone, including newly registered Yoda users, to submit a data
request, a public iRODS collection named "datarequests-research" must be
created. When a data request is submitted through a web form by a researcher, a
subcollection is created which will act as a folder for all files related to the
research proposal. The data request and research proposal is then saved to this
subcollection as a JSON-formatted file.

Because researchers only have ownership of subcollections they themselves have
created, they cannot access data requests by other researchers.

### Management and review of data requests
Project managers and data managers must be able to view all submitted data
requests and associated data (e.g. reviews).
They are enabled to do so by membership of, respectively, the
"datarequests-research-datamanagers" and "datarequests-research-project-managers"
groups. Membership of these groups grant the appropriate permissions on the
public collection mentioned above (these include read and write permissions).
Because these permissions are recursive, they also apply to the subcollections
made by researchers.

Upon assignment of a research proposal for evaluation to a DAC member, the DAC
member is granted read and write permissions on the subcollection in which the
research proposal is stored.

DAC membership is determined by membership of the
"datarequests-research-data-access-committee" group, which acts as a pool from
which the data manager may pick an appropriate member.

A DAC member can evaluate a research proposal through a web form. The evaluation
is saved as a JSON-formatted file in the subcollection that also holds the
research proposal itself.

Because multiple research groups may use a Yoda instance, multiple data manager
and DAC groups may be created so that data requests meant for data of a
particular research group can be handled by data managers associated with that
research group.

### Final evaluation of research proposals
A project manager can approve a research proposal through a web form that sets
the value of the status AVU of the research proposal subcollection to
"approved".

### Creation of DTAs
After the data request has been approved, the data manager creates a DTA and
adds it as a PDF file to the subcollection (through a web form). The researcher
will receive a request to upload as signed copy of this document.

### Approval of DTAs
The DTA created by the data manager is made available to the researcher. Once
the researcher has created a signed copy of the document, he can upload it
through a web form. The signed copy is saved in the subcollection. The data may
now be made available to the researcher by the data manager.

## Data assessment only (DAO) requests

DAO requests follow the procedure of regular data requests, as described above,
excluding the project manager's preliminary review, the data manager review, the
DAC review, and the research proposal preregistration. In other words, after
submission, a DAO request is immediately offered to the project manager for
final evaluation, after which the procedure is identical to regular data
requests.
