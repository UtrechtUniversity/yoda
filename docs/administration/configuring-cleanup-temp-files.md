---
parent: Administration Tasks
title: Configuring Cleanup functionality temporary files
nav_order: 13
---
# Configuring cleanup functionality of temporary files
Instruction on how to configure functionality to select identify temporary files in the research area.
It enables the possibility to show a list of temporary files and delete them individually or as a selection.

## Background
When using specific systems certain files (or file-types) get introduced.
These files have no relation whatsoever to the actual data of the research at hand. They merely get produced by the system or the tools used.  
Before entering the vault research data requires to be cleaned of these files as they serve no purpose. This can be a painstaking excercise.
Therefore, Yoda is equipped with a powerful tool that enables users to find these files easily and remove them in a simple manner if so required.

As temporary files can differ for different Yoda-systems it is possible to configure which files are considered superfluous. Thus, making this functionality flexible and effective for any user.

## Defining selection masks
It is possible to define masks that describe a certain file/type.  
The mask(s) will be used to select the corresponding files and show to a user.


### Mask - find specific files
It is possible to search for files that have a specific name.  
For example:  

```  
    mask definition: 'Thumbs.db'  ```
The mask will search exact matches of the filename 'Thumbs.db'.  


### Mask - use of wildcards
It is possible to use all common wildcards in the creation of a mask.  
For example:

```  
    mask definition with wildcard:  '._*''  ```
The mask will search for files whose name match the given wildcards.


### Multiple masks
Masks can be added by concatenation being sepecated by a comma.

```  
    multiple masks in mask defintion: '._*','Thumbs.db'  ```

## Configuring the variable
When creating a new Yoda instance, setup variable 'cleanup_temp_files' in the group_vars as explained in [Configuring Yoda](configuring-yoda.md) and run the playbook.  
Alternatively, you can choose to pass the variables with the *--extra-vars* option every time when running the Ansible playbook.
The development group_vars contains examples for all of the variables.



## Default value
When deploying Yoda the default value of this variable contains following masks:  

- '._*'         # MacOS resource fork  
- '.DS_Store',    # MacOS custom folder attributes  
- 'Thumbs.db'     # Windows thumbnail images


## Usage
The research module offers an option to activate the action menu has a specific menu option 'Cleanup temporary files'.  
