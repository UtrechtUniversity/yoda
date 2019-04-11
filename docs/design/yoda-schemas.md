# Layout of involved schemas within YoDa #

Different communities can have different metadata.

Each YoDa instance has a default layout.
When no category (=community) is set for any specific group, the default form (and consequently) schema's apply.


## Folder layout for category dependent schemas ##
Central folder for all configurational and statuent files related to metadata is:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/zone/yoda/schemas


Category (=community) dependency is dealt with by using subfolders like:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/zone/yoda/schemas/ilab

In this case ilab is the name of community "ilab".


Within the software presence of category configurations is always checked for at first.  
If not available then the fallback is to the default configuration:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/zone/yoda/schemas/default


## Involved files and their purpose ##

Each folder will hold the following files:

### - metadata.JSON ###
Configuration for the metadata form as used for a community.   
Both research and vault xsd's are derived from this JSON-file.

### - research.XSD ###
Requirements for metadata living in the <ins>research area</ins>   
There is a less strict regime for metadata within
Only when entering metadata into the vault, these stricter rules will be effectuated.

### - vault.XSD ###
Requirements for metadata entering the <ins>vault area</ins>.  
Equal to reseach.xsd. However, all required data is now effectuated.
Data package are not accepted into the vault when metadata does not comply to the corresponding vault.xsd


### - langdingpage.XSLT
The landing page is generated from this extensible stylesheet.

### - datacite.XSLT
For publication purposes to DataCite an XML conforming to the DataCite Schema v4 is generated with this extensible stylesheet.


### - avu.XSLT ##
This XSLT is used to add  AVU representations within iCat equal to yoda-metadata.xml.
This is used for search functionality eg.  
In order to make a clear distinction between user-entered data and system data, the user data is prefixed with 'usr_' when added as an AVU to iCat.
