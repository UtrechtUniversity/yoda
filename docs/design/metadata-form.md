# Metadata form
## Introduction
A Yoda instance holds research information regarding communities (categories).  
The type of research data can differ between communities.  
Metadata, that has to be registered together with research data, can differ as well between communities.  
Yoda supports communities to use their own metadata accompanying their research by giving them the support of a specific metadata form. If no form exists for a specific community then the standard metadata form is used.

## Generic implementation
The metadata form handling is technically implemented in a generic manner.

Within YoDa is it used in
- RESEARCH area    
to view/edit/add metadata for a dataset that will be placed in the vault. All in terms of the corresponding community
- VAULT area  
to view/edit/add the metatadata that accompanied a datasets when accepted for the vault. All in terms of the corresponding community
- DATAREQUEST module
Given the generic implementation of the form it is utilised in a whole different context for the DATAREQUEST module within YoDa.

*Only the Research and Vault implementation is discussed in this document.*

## Form functionality
The metadata form handling is implemented in a generic manner.   
In itself the generic metadata form deals with two situations, i.e.
- an editable form in which users can edit/add metadata to a datapackage
- a readonly view on this metadata as previously entered by a researcher

What the generic (metadata) form deals with:
- Presenting a form for the metadata of a specific datapackage where the elements on the form are configurable dependent on category
- A default metadata form configuration when no metadata form configuration exists for a category
- Possibility to have dependencies between elements on the form in order to form clear relations between the data
- Determining completeness of the form and giving proper indications to the user dependent on the category a datapackage belongs to
- Determining validity of the metadata form data dependent on the category a datapackage belongs to
- Saving the metadata to a file in XML format within the datapackage (called yoda-metadata.xml)
The file that can be edited via web disk as well by users with sufficient permissions
- When data is saved correctly add the metadata to iCat system as AVU’s to the corresponding datapackage information as well. This so these metadata entries can be searched by users
- Offering possibilities to, after correctly/successfully validating a metadata set, the result can be used for further actions.  Like the ability
  - to bring a datapackage / metadata to the vault from within the dynamic storage environment
  - to save several metadata files, with unique names, within the vault
- readonly view on metadata for a datapackage



*REACT FORM*   
Within YoDa, REACT is the center for metadata form handling. It gives the development team more flexibilty in extending form possibilities.  


REACT relies on JSON data and JSON validation schema’s.  
Within YoDa metadata is kept in XML (filename is yoda-metadata.xml).
That is why internally transformations will have to take place from JSON to XML and vice versa.

Data validation (when submitting metadata for the vault) will still take place based on XSD’s.

**Yoda metadata is still saved in XML and as such available/accessible for the enduser.**


# Integral part of Yoda

## React-form
In essence React-form is a fully configurarable form handler that is based on javascript and JSON schema.  
Fields can be configured using javascript classes.  
The form can be fully integrated in an application like for instance YoDa.

- Data can be exported (posted) to the application's backend
- Data can be imported into the form and presented in the form's fields

## YoDa integration

### Import yoda-metadata.xml and presentation in the form
YoDa-backend serves the frontend in creating a page holding the react form as a fully integrated part of YoDa.  
metadata.JSON holds the full definition of the form and is used for validation purposes as well.  
yoda-metadata.xml, the file that holds previously saved metadata, is transformed in terms of the metadata.JSON so the form can present the data.

### Export (JSON to XML)
When a user fills out the form and presses 'Save', the data is posted to the indicated backend.
This JSON response is transformed into the collection specific yoda-metadata.xml.  


### Deviations from standard React form
YoDa has some clear deviations from the standard functionality of React form. This to be able to mimic the behaviour of the preceiding (own development) form that did not use JSON form yet.

#### Default handling of React form is that when fields are clonable they are initially not visible.
Only after hitting the (add) button they become visible.  
There are challenges in correctly initializing array fields.

Our own YoDa form requires clonable fields to be present in the form already.


### Specific options menu depending on working in research or vault area
Depending on the area/module a user is working in, different options become available in the options menu.

#### Research area
'To vault' functionality  
Request a dataset in the research area to be saved into the vault.

#### Vault area
'Publish' functionality  
Request publication of a dataset in the vault.



# Basic structure

The metadata form is based on React library (https://reactjs.org/)  a javascript library intended for frontend purposes.

This is fitted into the place where the (now obsolete) previous version of metadata handling was situated.  
React replaces the older metadata handling processes completely.


##  Required files and purposes
- React library javascript library.  
This forms the generic basis for the frontend.  
 
- metadata.json - JSON schema  
A JSON file that mainly holds the structural definition of the metadata form as well as mandatoriness.  
This file has been designed for the Yoda implementation and is based on the JSON schema specification (https://json-schema.org/).
The metadata.json file mainly holds all information for the metadata form:  
  1. Declaration of groups of elements
  2. Element names corresponding to the XSD
  3. Element specifics intended for the researcher, like
    - Label of the input element
    - tooltips when hovering over the field
    - Default value when no metadata has been saved yet
  4. Mandatoriness of metadata
  Metadata fields can be configured as being mandatory when requested to be accepted in the vault.
  Special mandatoryness-rules apply for compound fields and subproperty structures.
  This is discusses further in this document.

- research.XSD  
  The research  XSD is used to validate and describe metatadata that is in the research area.
  This XSD is in fact a translation of the corresponding JSON schema.  
  To be able to do so, an application JSONS2XSD was created which is described in another design document.

- vault.XSD  
The vault  XSD is used to validate metadata before it is allowed to be entered in the vault area.  
This XSD is in fact a translation of the corresponding JSON schema.  
To be able to do so, an application JSONS2XSD was created which is described in another design document.

- yoda-metadata.xml  
Holds, in XML format, the metadata as entered by the user.  
This, either after a save action of the user from within the form, or when edited directly when using a WEBdav client.  
The XML data should comply to the corresponding XSD before the metadata can be accepted into the vault.


## Complex Data structures

### Subproperty structure
Subproperties designate a structure consisting of
1. one lead element
2. N elements (subproperties) linked to the lead element organised as one group

The lead elemenent can be of every type as mentioned earlier.

#### Implicit mandatoriness
Subproperties cannot exist without the lead information being present.
Saving subproperties that have no lead-data will be deleted when saved.
I.e. the lead information becomes implicitly mandatory when subproperty data exists.

#### Mandatory subproperty within a subproperty structure
A subproperty can be configured as being mandatory.
This rule only applies when lead information is present.

#### Multiplicity/cloning for subproperty structure:
The entire structure can be cloned (if set to multiple within the JSONS).
Subproperties themselves can be cloned if configured in JSONS
Compound fields (see further) can be treated as subproperties and all the above rules will be applicable to these a well (and their own compound properties will be maintained as well)

#### Compound elements
A compound element is an element that consists of several, at least one, related elements.
They are considered to belong together and in that sense treated in that manner.

#### Multiplicity/cloning of compounds
Entire element can be made cloneable – thus cloning the total structure in its entirety

Each individual constructing element within the compound can be made cloneable as well– thus cloning the element within its compound element.

**Implicit mandatoriness when compound is partly filled.**
If one element of a compound is filled, all the others have to be filled as well. These are considered mandatory as well.
Partly filling a compound is not accepted as being valid information

### Compound field as a subproperty

A compound field can be regarded as being a single element. Therefore, it can also be used as a a subproperty.
This is especially useful when the need exists to save the relation of one leading element and a set of information that belongs together.

#### Mandatoriness
Again, if one of the compound elements fields holds data, the other element(s) become mandatory as well. I.e. data cannot be saved when a compound field is not fully filled out.


#### Multiplicity/cloning entire compound
A compound field can be regarded as one element.
Therefore, it can be cloned in its entirety adding one (or more) cloned compounds to the lead element.

#### Multiplicity – cloning element(s) within a compound
As a compound is constructed with normal elements it is possible to add cloning to each or one specific element within a compound element.


### General validation rules for complex structures

Subproperties cannot exist without a lead/main property being present.
I.e. A subproperty structure without lead information is regarded as incomplete information.
As a result the corresponding datapackage will not be accepted for the vault.

* A subproperty can be configured as being mandatory.*

However, this rule is only valid when the corresponding lead element is filled.
In other words, eventhough a mandatory rule exists on a subproperty, the actual subproperty-structure could still be configured as being none-mandatory for the vault.

* Completeness of a compound field*

Compounds are constructed of separate fields but can be regarded as one element.
If one element of a compound field holds a value the other n fields should hold a value as well.

* Completeness of a compound field as a subproperty*
Compound fields within a subproperty structure follow the same rules as on highest level.
I.e. when one element is filled, all elements must be filled.



# Integration of REACT form within YoDa #
The file   

&nbsp;&nbsp;&nbsp;&nbsp;*YoDa-module*/app/index.js  

holds all YoDa-application specific javascript code to tweak the REACT form to the needs of the application.  
It handles all YoDa specific situations where the REACTform is involved.  
It integrates it within the YoDa application.

Code changes do not directly take effect.  
In order to effectuate, use:

./node_modules/.bin/webpack -d  
in:  
/var/www/yoda/yoda-portal/modules/research

Since there is a separate vault module this will hold its own /app/index.js
