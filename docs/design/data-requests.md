# Data requests

## Introduction
This technical design document describes an approach to implementing support for
the submission, review and approval of requests to obtain research data stored
in Yoda.

## Definitions
-   **Research group** A group of researchers belonging to a particular research
lab or otherwise collaborating on a common research goal. E.g. the Brain
Morphology Lab.

## Functional description
The supported workflows are as follows:

### Submission of data requests
A researcher seeking to obtain research data stored in Yoda must be able to
submit a request for this data.

The request must belong to a research proposal, which is submitted along with
the data request. The research proposal must describe the purpose for which the
researcher wants to obtain the requested data.

### Management of data requests
A data manager assigned as a custodian of (certain) data stored in Yoda must be
able to see submitted requests for this data.

The data manager must be able to delegate the evaluation of the research
proposals belonging to these requests to one or more members of a Data
Management Committee (DMC). For example, given a research proposal on brain
morphology, the data manager may assign the evaluation of this proposal to a
specific DMC member with expertise in this area.

### Evaluation of research proposals
A DMC member must be able to view research proposals assigned to him for
evaluation and must be able to register his evaluation of the research proposal.

### Approval of research proposals
A representative of a research programme's or study's Board of Directors must be
able to approve a research proposal based on the evaluations given by one or
more DMC members.

### Evaluation of data requests
Once a research proposal has been approved, the data manager must be able to
review a data request belonging to this proposal. This is done to ensure that
the requested data is within scope of the approved research proposal.

### Approval of data requests
If, after reviewing the data request, the data manager does not object to the
release of the requested data, he must be able to approve the data request.

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
may release the requested data to him. However, the means by which the data is
transferred to the researcher is outside of the scope of the data request
module.

## Technical description
To keep the complexity of the module to a minimum, existing Yoda functionality
and modules are used to implement the functional requirements.

### Submission of data requests
To allow anyone, including newly registered Yoda users, to submit a data
request, a public iRODS collection (named, for example, "datarequests") must be
created. When a data request is submitted through a web form by a researcher, a
subcollection is created which will act as a folder for all files related to the
research proposal. The data request and research proposal is then saved to this
subcollection as a JSON-formatted file.

Because researchers only have ownership of subcollections they themselves have
created, they cannot access data requests by other researchers.

### Management of data requests
Data managers must be able to view all submitted data requests. They are enabled
to do so by membership of a group (e.g. "brainmorphlab-datamanagers"; see Group
Manager) that has group manager permissions on the public collection mentioned
above (these include read and write permissions). Because these permissions are
recursive, they also apply to the subcollections made by researchers.

To assign a research proposal for evaluation to a DMC member, the data manager
can give the DMC member read and write permissions on the subcollection in which
the research proposal is stored. DMC membership is determined by membership of a
particular group (e.g. "brainmorphlab-dmc"), acting as a pool from which the
data manager may pick an appropriate member.

Because multiple research groups may use on a Yoda instance, multiple data
manager and DMC groups may be created so that data requests meant for data of a
particular research group can be handled by data managers associated with that
research group.

### Evaluation of research proposals
A DMC member can evaluate a research proposal through a web form. The evaluation
is saved as a JSON-formatted file in the subcollection that also holds the
research proposal itself.

### Approval of research proposals
Board of Directors (BoD) representatives also belong to a particular group (e.g.
"brainmorphlab-bodr". They have the same rights as those in the data manager
group, thus allowing them to view the research proposal and the evaluations
of the reviewing DMC members.

A BoD representative can approve a research proposal through a web form that
sets the value of the approval_status AVU of the research proposal JSON file to
"approved".

### Evaluation of data requests
After the approval of a research proposal, the data manager evaluates the data
request.

### Approval of data requests
If the data manager approves the data request, the approval_status AVU of the
data request JSON file is set to "approved".

### Creation of DTAs
After approving the data request, the data manager creates a DTA and adds it
as a PDF file to the subcollection (through a web form). The requesting
researcher will receive a request to upload as signed copy of this document.

### Approval of DTAs
The DTA created by the data manager is made available to the researcher. Once
the researcher has created as signed copy of the document, he can upload it
through a web form. The signed copy is saved in the subcollection. The data may
now be made available to the researcher by the data manager.
