# Community dependent files for configuration of metadata handling

## Community dependency
Within YoDa, research is supported via groups;  administrative entities declaring which persons are allowed to participate in that perticular research.
 
Each group within YoDa belongs to a community. A community (=category ) can hold multiple groups.

Different communities may require community specific metadata to be added to their research datasets.
YoDa is designed in such a way that each community can have its own metadata definition. It accommodates handling of community dependent metadata though configuration of the generic metadataform.

If such a community specific definition is not present the system will fall back unto the default definition each YoDa instance is always equipped with.

The metadata definition is declared in JSON schema’s.

A metadata configuration file should always include all information that is required to be able to publish the research datapackage, including its metadata.
The exact fields can be found on datacite.org


## Folder layout for category dependent schemas
Central folder for all configurational and statuent files related to metadata is:

`/zone/yoda/schemas`


Category (=community) dependency is dealt with by using subfolders like:

`/zone/yoda/schemas/ilab`

In this case ilab is the name of community "ilab".

Within the software presence of category configurations is always checked for first.  
If not available then the fallback is to the default configuration:

`/zone/yoda/schemas/default`

## Involved files and their purpose
Each folder will hold the following files:

### metadata.json
Configuration for the metadata form as used for a community.   
Both research and vault xsd's are derived from this JSON-file.

### research.xsd
Requirements for metadata living in the <ins>research area</ins>   
There is a less strict regime for metadata within
Only when entering metadata into the vault, these stricter rules will be effectuated.

### vault.xsd
Requirements for metadata entering the <ins>vault area</ins>.  
Equal to reseach.xsd. However, all required data is now effectuated.
Data package are not accepted into the vault when metadata does not comply to the corresponding vault.xsd

### langdingpage.xsl
The landing page is generated from this extensible stylesheet.

### datacite.xsl
For publication purposes to DataCite an XML conforming to the DataCite Schema v4 is generated with this extensible stylesheet.

### avu.XSLT
This XSLT is used to add  AVU representations within iCAT equal to yoda-metadata.xml.
This is used for search functionality eg.  
In order to make a clear distinction between user-entered data and system data, the user data is prefixed with 'usr_' when added as an AVU to iCat.
