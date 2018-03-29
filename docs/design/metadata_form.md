# Metadata form

## Introduction
A Yoda instance holds research information regarding communities (categories).
The type of research data can differ between communities.
Metadata that has to be registered together with research data that can differ as well between communities.

Yoda supports communities to use their own metadata accompanying their research by giving them the support of a specific metadata form. If no form exists for a specific community then the standard metadata form is used.

## Generic implementation
The metadata form handling is generically implemented. It can be used within several situations/contexts and is used eg. both within the dynamic storage area as well as the vault.

In itself the generic metadata form deals with two situations, i.e.
- an editable form in which users can edit/add metadata to a datapackage
- a readonly view on this metadata as previously entered by a researcher

What the generic metadata form deals with:
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


## Metadata form: files involved

A metadata form is constructed with the contents of following files.

**formelements.xml**

An xml file that mainly holds the structural definition of the metadata form as well as mandatoriness.
This file has been designed for the yoda implementation and is not based on any standard apart from XML.

**an XSD file**

The XSD holds requirements and restrictions for the actual data in the form
This file complies to the XSD standard as used for validating data in XML structures.
Each Yoda-instance has a default set called default.xsd and default.xml
Category dependency is introduced by adding an XSD and XML file with the category name.
ilab.xsd and ilab.xml could be the constructing files for a metadata schema for a category call ilab.

The researcher, nor any other user, can see or change the formelements or XSD files.
This is done by an administrator.

**yoda-metadata.xml**

A third file holds the actual metadata as entered by the researcher and is kept within the corresponding datapackage.
The file is editable for the researcher in dynamic storage area when not in a locked state. It is editable by any user that is not limited to readonly-rights.
The structure of the file must comply to the XSD that applies.
If not, the metadata form cannot be loaded.

### Getting the correct file paths
All three files are required for the generic functionality to work correctly.
iRods offers the specific situational filenames for correct configuration of the metadata form.
The situation (dynamic storage, vault etc) is passed and based upon the full pathname of a datapackage which gives iRODS the required insight:

$formConfig = $this->filesystem->metadataFormPaths($rodsaccount, $fullPath);
This returns a number of parameters but the three of importance are:

**xsdPath**

Holds the path to the XSD to be used.
Either the category specific or the default XSD.

**formelementsPath**

Holds the formelements file involved.
Either the category specific or the default formelements.

**metadataXmlPath**

Holds the path to the metadata file that holds the data as entered by a Yoda user.
In the dynamic storage this would be yoda-metadata.xml file.

## formelements.xml explanation

Formelements.xml mainly holds information relevant for the ‘user experience’.
In XML format formelements.xml holds:
1. Declaration of groups of elements
2. Element names corresponding to the XSD
3. Element specifics intended for the researcher, like
  - Label of the input element
  - tooltips when hovering over the field
  - Default value when no metadata has been saved yet

4. Mandatoriness of metadata
Metadata fields can be configured as being mandatory when requested to be accepted in the vault.

Subproperties can be made mandatory for the vault.
Compounds cannot be made mandatory.
Implicit rules apply for subproperties/compounds in special structures as will become clear further on.

### File location
formelements should be put in the following iRODS collection:
/zone/yoda/formelements

### Formelements examples

**1. Declaration of groups of elements**

![Image metadata form Descriptive group](http://via.placeholder.com/750x150)

ElementGroups such as ‘Descriptive’ make a form more readable and understandable. Especially when the form is elaborate.

Within XML formelements.xml ElementGroups are added as follows:

```xml
<?xml version="1.0" encoding="utf-8"?>
<formelements>
	<Group name="Descriptive">
	</Group>
	<Group name="General">
	</Group>
</formelements>
```

This will create a metadataform consisting of two groups: “Descriptive” and “General”. Elements within the Group tags will belong to that group in the form.
The order of appearance in formelements.xml is the order the groups are shown in the metadataform itself.

**2. Element names corresponding to the XSD**

```xml
<?xml version="1.0" encoding="utf-8"?>
<formelements>
	<Group name="Descriptive">
		<Title></Title>
		<Description></Description>
	</Group>
	<Group name="General">
	</Group>
</formelements>
```

Every element other than the reserved elements (formelements, Group, label, help and attribute class=”compound”) correspond to an identifier of metadata field.
In these examples eg. ‘Title’ and ‘Description’ are identifiers of the element.
These correspond to the same identifier in the XSD. Thus making it possible to combine both files (‘formelements’ and ‘xsd’) to be able to construct a metadata form.
Both from their own perspective.
The XSD holds information regarding limitations/requirements of the actual data as added by the user.

**3. Labels, tooltips/help text**

For the datapackage title element following construction

```xml
	<Group name="Descriptive">
		<Title>
			<label>Data Package Title</label>
			<help>The title of your data package</help>
		</Title>
```
The help text will become visible when hovering over the label of the field.

**4. Default values**

When opening the form and no corresponding yoda-metadata.xml exists, the metadataform will present the default value. If configured.
In below example the default value for Retention Period in this metadata form is 10.

![Image of filled in Retention Period field](http://via.placeholder.com/750x150)

```xml
		<Retention_Period>
			<label>Retention Period</label>
			<help>The minimal number of years the data will be kept in the archive</help>
			<default>10</default>
			<mandatory>true</mandatory>
		</Retention_Period>
```

**5. Mandatoriness**

Mandatoriness signifies that metadata must be present when requesting acceptance for the vault.
If a mandatory field  holds no value, the request will not be accepted by the system and the user is asked to fill out the missing data.

```xml
		<Retention_Period>
			<label>Retention Period</label>
			<help>The minimal number of years the data will be kept in the archive</help>
			<default>10</default>
			<mandatory>true</mandatory>
		</Retention_Period>
```

![Image of empty Retention Period field](http://via.placeholder.com/750x150)

![Image of red lock](http://via.placeholder.com/150x150)
signifies that the corresponding field is mandatory for the vault.

![Image of red lock with green mark](http://via.placeholder.com/150x150)
signifies that the field is mandatory and the field is filled out correctly

These indications are actual directly after saving or showing the metadata form.
These are not real time indications so changes by the user are not followed and indicated directly (in real time).

## XSD explanation
The XSD lays down the requirements for the data the metadata has to comply to.
It describes properties as length and datatype.
For selects it determines all the selectable options.
Thus, the data in the form can be validated against the XSD.
The XSD does not hold information regarding mandatoriness of data for the yoda-implementation.

### File location
All XSD’s should be put in the following iRODS collection:
Location: /zone/yoda/xsd

### Element types
Any form consists of input elements or fields.  
In yoda the metadata form is comprised of the following elements:

- text elements: simple length restricted input elements for text, numeric and uri’s
- multiline text elements also known as text area’s
- select elements that can bring up configurable options
More specifically with a search possibility in the element through the option list
- date selection elements

### Element type specifics
The identifiers as mentioned in the formelements.xml file are present in the XSD as well.
Thus, it is possible to combine the information and distinguish data specifics of all the elements within the metadata form.

### In the XSD file:
All elements are assigned a type. Either a primitive type or a type defined in the XSD itself. The specifics of the primitive types can be found in the definition of the XSD standard at: https://www.w3.org/TR/xmlschema-2

**Type = xs:date**
Brings up a date picker element.
This field will be validated against the primitive xs:date type.

**Type = stringURI**
Brings up a text field in the metadata form with a maxLength as set in the simpleType definition in the XSD. This text field based on the primitive type xs:anyURI, but with an extra restriction that the max length is 1024 characters. URI do not have an official max length but in practice longer URIs can be problematic.
The simpleType can be modified if required.
```xml
        <xs:simpleType name="stringURI">
            <xs:restriction base="xs:anyURI">
                <xs:maxLength value="1024"/>
            </xs:restriction>
        </xs:simpleType>
```

**Type = stringNormal:**
Brings up a text field in the metadata form with a maxLength as set in the simpleType definition in the XSD. This text field can hold any data and will only be checked for a max length of 255 characters.
```xml
        <xs:simpleType name="stringNormal">
                <xs:restriction base="xs:string">
                        <xs:maxLength value="255"/>
                </xs:restriction>
         </xs:simpleType>
```

**Type = xs:integer:**
Brings up a text field that can only hold numeric data.
Specifically this is limited to 10 digits.
This number will be validated against the primitve type xs:integer.

**Type = xs:anyURI:**
Will bring up a text field with a length of 1024 characters.
The URI will be validated against xs:anyURI definition

**Type = stringLong:**
Brings up a text area element.
The maximum length is taken from the simpleType definition as configured in the same XSD and the data will be validated accordingly.
```xml
        <xs:simpleType name="stringLong">
                <xs:restriction base="xs:string">
                        <xs:maxLength value="2700"/>
                </xs:restriction>
         </xs:simpleType>
```

**Type = optionsAnyName:**
Any type prefixed with the word “options” should be associated with a list of values.
This will bring up a select field with options as configured in the simpleType definition in the XSD.

```xml
  <xs:simpleType name="optionsNameIdentifierScheme">
    <xs:restriction base="xs:string">
      <xs:enumeration value="ORCID"/>
      <xs:enumeration value="DAI"/>
      <xs:enumeration value="Author identifier (Scopus)"/>
      <xs:enumeration value="ResearcherID (Web of Science)"/>
      <xs:enumeration value="ISNI"/>
    </xs:restriction>
  </xs:simpleType>
```

**Reserved/protected words:**
A developer can add changes to XSD’s. Create own simpleTypes etc.
The following list contains words not to be used and defined as simpleTypes:

- structSubPropertiesOpen
- structSubPropertiesClose
- structCombinationOpen
- structCombinationClose


### Multiplicity
Some form data data can be present in multiple instances.
This can be achieved by using ```maxOccurs="unbounded"``` on the element level in the XSD. (or any other integer value if a specific restriction in multiplicity exists for a given element)

**Important note:**
minOccurs cannot not be used and should remain set at zero at all times.
When set to 1 (or more) submitting an incomplete metadata form by a user will lead to failure opening the metadata form again.
XSD-validation is the first step when opening a metadata form. As the metadata that was submitted is missing data, the form will show the validation errors found instead of the metadata form itself.
As it is not expected the user to fill out a metadata form completely in one go it is impossible to add manditoriness in the XSD.
Consequently, manditoriness of data is moved to formelements.

### Data validation
In general, when submitting a datapackage to the vault, its metadata is validated if correct and complete:
1. Test for validity
This is a test directly against the corresponding XSD.
2. Test for completeness
This is a test on the basis of mandatory-settings for each element in formelements.


## Example of a metadata field XSD and formelements

![Image of locations covered metadata field](http://via.placeholder.com/750x150)

Location(s) covered can be entered multiple times.
The XSD holds:

```xml
<xs:element name="Location_Covered" type="stringNormal" minOccurs="0" maxOccurs="unbounded"/>
```

The stringNormal type signifies a normal input with length 255 (see XSD simpleTypes definitions).
```maxOcccurs=”unbounded”``` will add the plus-sign to the form element. Thus allowing for cloning of the element and giving the element the possibility to hold multiple values.

When data validation occurs it is also validated against maxOccurs.
maxOccurs can have any value as accepted by XSD standard, but currently only 1 or unbounded make sense.

Corresponding formelements entry could look like the following:

```xml
<Location_Covered>
      <label>Location(s) covered</label>
      <help>Indication of the geographical entities, like countries, regions and cities, covered with this data package (English naming convention preferred)</help>
</Location_Covered>
```

This element could be made mandatory by adding ```<mandatory>true</mandatory>``` on the same level as label and help.


## Special structures of elements
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

#### Subproperty Structure
The structure is designated by a ```<Properties>``` section. (Stylesheet implementations count on this being present).

For example:
```xml
<Related_Datapackage>
<Title>
<label>Predecessing Data Package</label>
<help>Title of the previous version of this data package</help>
</Title>
<Properties>
<Persistent_Identifier>
<label>Persistent Identifier</label>
<help>Persistent identifier of the previous version of this data package</help>
</Persistent_Identifier>
<Persistent_Identifier_Type>
<label>Type of Persistent Identifier</label>
<help>Type of Persistent identifier of the previous version of this data package</help>
</Persistent_Identifier_Type>
</Properties>
</Related_Datapackage>
```
In the above example a lead element ‘Related Datapackage’ has two subproperties “Persistent Identifier” and “Persistent identifier type”

#### Multiplicity/cloning for subproperty structure:
The entire structure can be cloned (if set to multiple within the XSD).
Subproperties themselves can be cloned if configured in XSD.
Compound fields (see further) can be treated as subproperties and all the above rules will be applicable to these a well (and their own compound properties will be maintained as well)

### Compound elements

A compound element is an element that consists of several, at least one, related elements.
They are considered to belong together and in that sense treated in that manner.

In order to distinguish combination fields from other elements a compound element is created by adding class=compound to the given element required to be a compound element.
In the next example License and Link webpage belong together (one license has one related webpage):

![Image of license and webpage link metadata field](http://via.placeholder.com/750x150)

Formelements.xml for the above example could look like the following:
```xml
<License class="compound">
                        <Name>
                          <label>License</label>
                          <help> The license under which you offer the data package for use by third parties. Preferred value is "CC By 3.0"</help>
                          <default>To be defined</default>
                        </Name>
                           <URL>
                             <label>Link Webpage</label>
                             <help> A link to a webpage describing the license and its conditions. In case of CC By 3.0 'https://creativecommons.org/licenses/by/3.0/'</help>
                           </URL>
</License>
```

Corresponding XSD:
```xml
<xs:element name="License" minOccurs="0" maxOccurs="unbounded">
<xs:complexType>
                <xs:sequence>
                     <xs:element name="Name" type="stringNormal" minOccurs="0" maxOccurs="1"/>
                     <xs:element name="URL" type="stringURI" minOccurs="0" maxOccurs="unbounded"/>
                </xs:sequence>
            </xs:complexType>
</xs:element>
```

#### Multiplicity/cloning of compounds
Entire element can be made cloneable – thus cloning the total structure in its entirety
Given XSD (above) shows how on the highest level (maxOccurs=”unbounded”)
So several license/URL combinations (i.e. compounds) could be added.

Each individual constructing element within the compound can be made cloneable as well– thus cloning the element within its compound element.
In the above example it is even possible to add multiple URL’s per License name
The name itself cannot be cloned.

**Implicit mandatoriness when compound is partly filled.**
If one element of a compound is filled, all the others have to be filled as well. These are considered mandatory as well.
Partly filling a compound is not accepted as being valid information


#### Label for compound field main level
![Image of collection process with start date and end date](http://via.placeholder.com/750x150)

To add an overall label to a main level compound field add <label> tag just within the designating compound tag in formelements:
```xml
    <Collected class="compound">
      <label>Collection process</label>
      <help>Indicate when collecting the data for this data package started</help>
      <Start_Date>
        <label>Start Date</label>
        <help>Indicate when you've started collecting the data for this data package (YYYY-MM-DD)</help>
      </Start_Date>
      <End_Date>
        <label>End Date</label>
        <help>Indicate when you've finished collecting the data for this data package (YYYY-MM-DD)</help>
      </End_Date>
    </Collected>
```



### Compound field as a subproperty

A compound field can be regarded as being a single element. Therefore, it can also be used as a a subproperty.
This is especially useful when the need exists to save the relation of one leading element and a set of information that belongs together.
For instance the relationship between a person (lead element) and the ID and type of ID that always go together.

![Image of contributors to data package with subproperties](http://via.placeholder.com/750x150)

Type of persistent identifier and persistent identifier are a compound field in this subproperty structure.

```xml
    <Contributor>
      <Name>
        <label>Contributor(s) to Data Package</label>
        <help>The name(s) of the persons who have contributed to this data package</help>
      </Name>
      <Properties>
        <Contributor_Type>
            <label>Contributor Type</label>
            <help>See dataCite</help>
            <mandatory>true</mandatory>
        </Contributor_Type>
       <Affiliation>
          <label>Affiliation</label>
          <help>The organizational or institutional affiliation of the creator</help>
          <default>Utrecht University</default>
        </Affiliation>
        <Identifier_Person class="compound">
          <Name_Identifier_Scheme>
            <label>Type of Persistent Identifier</label>
            <help>What type of persistent person identifier</help>
          </Name_Identifier_Scheme>
          <Name_Identifier>
            <label>Persistent Identifier</label>
            <help>Persistent identifier of contributor (e.g. an ORCID, DAI, or ScopusID)</help>
          </Name_Identifier>
        </Identifier_Person>
      </Properties>
    </Contributor>
```

XSD:
```xml
<xs:element name="Creator" minOccurs="0" maxOccurs="unbounded">
   <xs:complexType>
     <xs:sequence>
       <xs:element name="Name" type="stringNormal" minOccurs="0" maxOccurs="1"/>
       <xs:element name="Properties" minOccurs="0" maxOccurs="1">
         <xs:complexType>
           <xs:sequence>
             <xs:element name="Affiliation" type="stringNormal" minOccurs="0" maxOccurs="unbounded"/>
             <xs:element name="Identifier_Person" minOccurs="0" maxOccurs="unbounded">
               <xs:complexType>
                 <xs:sequence>
                   <xs:element name="Name_Identifier_Scheme" type="optionsNameIdentifierScheme"               minOccurs="0" maxOccurs="1"/>
                   <xs:element name="Name_Identifier" type="stringNormal" minOccurs="0" maxOccurs="1"/>
                  </xs:sequence>
               </xs:complexType>
             </xs:element>
           </xs:sequence>
         </xs:complexType>
       </xs:element>
     </xs:sequence>
   </xs:complexType>
</xs:element>
```

#### Mandatoriness
Again, if one of the compound elements fields holds data, the other element(s) become mandatory as well. I.e. data cannot be saved when a compound field is not fully filled out.


#### Multiplicity/cloning entire compound
A compound field can be regarded as one element.
Therefore, it can be cloned in its entirety adding one (or more) cloned compounds to the lead element.

#### Multiplicity – cloning element(s) within a compound
As a compound is constructed with normal elements it is possible to add cloning to each or one specific element within a compound element.


### Label for compound field as subproperty

![Image of creator of datapackage with subproperties](http://via.placeholder.com/750x150)

To add an overall label to a subproperty level compound field add <label> tag just within the designating compound tag in formelements:

```xml
    <Creator>
      <Name>
        <label>Creator of Data Package</label>
        <help> The name of the person(s) who created (a version of) the data package</help>
        <mandatory>true</mandatory>
      </Name>
      <Properties>
       <Affiliation>
          <label>Affiliation</label>
          <help>The organizational or institutional affiliation of the creator</help>
          <default>Utrecht University</default>
          <mandatory>true</mandatory>
        </Affiliation>
         <Person_Identifier class="compound">
          <label>Persistent identifier</label>
          <Name_Identifier_Scheme>
            <label>Type</label>
            <help>What type of person identifier is used? </help>
          </Name_Identifier_Scheme>
          <Name_Identifier>
            <label>Identifier</label>
            <help>Identifier as it can be resolved on the appropriate service</help>
          </Name_Identifier>
        </Person_Identifier>
      </Properties>
    </Creator>
```
