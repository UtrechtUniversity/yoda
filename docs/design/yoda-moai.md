# Provisioning CKAN CATALOGS #

## Overview
![OVerview MOAI-CKAN](img/moai-ckan.png)


## MOAI
MOAI offers harvesting functionality following the OAI-PMH standard with the flexibility to serve different metadata prefixes.
Currently, for the YoDa application datacite is implemented as a metadata prefix.

## Provisioning MOAI database
When publishing datasets from within YoDa, the corresponding yoda-metadata.xml is put in a location where MOAI can read and process it.  
Each 5 minutes (configrable) the indicated folder (configurable) is scanned and newly published XML files are provisioned tot he internal sqlite database of MOAI.  
The data is prepared in the database as such that it is able to provide output in XML form, datacite format, on request of a harvester.
Any OAI-PMH harvester, able to ‘read’ datacite format, is able to harvest YoDa through the endpoint serviced by MOAI.

**Endpoint: moai/moai/**

## MOAI Technical:##
### Provision from YoDa  
*python -> yoda.py*  
The  script reads all yoda-metadata.xml files that have been published and are placed in a specific folder. After processing it puts the found content into the MOAI SQLITE database.

*Collection name as metadata for a dataset*  
A collection name defines an umbrella for different datasets to belong togehter.
It   
By exposing collection names through MOAI, it us possible for a harvester to draw conclusions regarding datasets from the same data supplier about datasets that belong together.  
Thus, multple datasets can setup a collection having the same 'purpose'.  
The nature of this purpose can be defined by the researchers/datamanagers themselves.  

In theory, equivalent collection names can exist over multiple YoDa instances.
Even within the same YoDa instance.  
No validation is performed by YoDa software itself.
So there is nog formal safeguarding/protection of the content of collection name.  
Harvesters should be (made) aware of that.  
Initially they should combine collections endpoint/collection 


select * from sets;  
select * from records;

### Deliver metadata in datacite format to harvesters  
*python -> datacite.py*  
Prepares the output data in such a way that the application data of YoDa, originally held in yoda-metadata.xml files, can be outputed to an XML response with datacite as a metadata prefix.


#  CKAN catalog
I-lab uses CKAN as basis for catalog functionality.  
CKAN is generic software that can be tailored to become an entirely blabla application.
It uses several modules / extensions to be able to form CKAN standard product into an application that can handle YoDa specific data.

## Harvest sources   
A harvest source is a configuration, added within CKAN, to instruct where to harvest for data and how to deal with the harvested data from the source (in this case YODA).  
This by passing information to the ckan module CKANEXT-OAIPMH (see further)

Harvest sources, which is functionality added to CKAN by 3rd party module ‘ckan-harvester’, is mainly a configuration holding:  
-endpoint  
-params to tell configure the source freely as an application programmer  
-harvest type (either CKAN/OAIPMH when OAI-PMH extension added)

CKANEXT HARVESTER uses a POSTGRESQL database to be able to harvest.  

## Harvesting stages
Harvesting is realised in following three stages:

- Gather stage  
Through OAI PMH gather all present datapackage and create a list of them in the postgresql database.

- Import stage  
One by one handle the list of gather Ids and add them tot he database as a JSON-object separately.

- Fetch stage  
The data that is fetched can now be processed and, in accordance with module CKANEXT-CUSTOM-THEME,  be saved into CKAN itself.
This has to be in alignment with the theme as the theme contains the ‘application’ and this needs to be ‘fed’ correctly from the database.  
This goes especially for the extra – fields.

The processing of the fetched data is dealt with within another extension. CKANEXT-OAIPMH.  
Thus, any party can tailor CKAN to its own wishes.  
This extension is under development by the YoDa-team: CKANEXT-OAIPMH


## CKAN Extension CKANEXT-OAIPMH
A generic component that currently is used for catalog applications iLAB and EPOS.  
It allows for harvesting through the OAI-PMH standard.  
CKANEXT-OAIPMH processes the harvested data that was collected at the endpoint within the harvest source.

Driven by the parameters as stated in the CKAN **harvest source** that initiated the harvest process, CKANEXT-OAIPMH module can be configured to treat data differently corresponding to the active configuration. Thus, supporting the possibility for totally different applications.  

In our case this component handles two entirey different sources for entirely different applications:  
1) EPOS, and  
2) ILAB

The differentiation can be made by passing the correct parameters into the Harvest source:

Configuration:   
*Voor ILAB datacite:*  
{"metadata_prefix": "datacite",  
"application": "ILAB"  
}

*EPOS iso metadataPrefix:*  
{"metadata_prefix": "iso19139",  
"application": "EPOS",  
"set":"~P3E9c3ViamVjdCUzQSUyMm11bHRpLXNjYWxlK2xhYm9yYXRvcmllcyUyMg"  
}


*EPOS datacite metadataPrefix:*  
{"metadata_prefix": "datacite",  
"application": "EPOS",  
"additional_info": "kernel4",  
"set":"~P3E9c3ViamVjdCUzQSUyMm11bHRpLXNjYWxlK2xhYm9yYXRvcmllcyUyMg"  
}
NB "set" is part of the OAIPMH standard

The CKAN-OAIPMH extension is programmed as such that it will provision CKAN based upon the above parameters.
Main differentation is the application. Currently EPOS and iLAB.


# Application specific handling

## iLAB
metadataPrefix = **datacite**  
The organisation linked to the harvest source is added to each datapackage as being the owning organisation (owner_org: see further CKAN fields).

Example ckan harvest source configuration:  
{  
&nbsp;&nbsp;"metadata_prefix": "datacite",  
&nbsp;&nbsp;"application": "ILAB"  
}


## EPOS
metadataPrefix = **ISO**

*-Owner organisation is determined from within harvested data*  
NO new organisations are added programmatically when processing the harvested data.  
Otto Lange, CKAN admin, controls this proces in the sense that he controls which organisations are known within CKAN.  
If a passed organisation is present in CKAN already, that organisation is used as owner organisatin.  
If not known within CKAN -> ‘Other lab’ is default.

Thus, organization ‘Other lab’ is an indicator of datapackages from unkown origins (from the point of view of CKAN).



*-Maintainer is derived from harvest source organisation*  
Similarly like in iLAB the harvest source organisation is used.
For iLAB the harvest source organisation is used as owner organisation of a datapackage.
FOr EPOS however, the harvest source organisation is used maintainer of the datapackage.
Consequence of this is that maintainer organisations need to be added to CKAN as organisations. Otherwise, it is not possible to add the organisation to a harvest source. And consequently use it as maintainer regarding the harvested datapackage.

        self.package_dict['maintainer'] = harvest_source.organisation
        self.package_dict['maintainer_email'] = harvest_source.organisation.email



*-Specific EPOS 'package reference' handling *  
Within the EPOS application there are 3 types of references regarding a package:

-supplement to  
-cites  
-references  

Within the harvested XML that minimal information is passed regarding these references.  
Therefore, lookup functionality is added to get more details via GFZ.


http://dataservices.gfz-potsdam.de/getcitationinfo.php?doi=http://dx.doi.org/' op basis van DOI

Example:  
http://dataservices.gfz-potsdam.de/getcitationinfo.php?doi=http://dx.doi.org/10.1007/s11214-010-9693-4

Based upon the received citation info, the CKAN package can be filled with more elaborate information.

This extra provisioning was deliberately created for EPOS handling - GFZ specifically.
In order run this functionality, it must be added to the corresponding harvest source configuration.


example configuration for harvest source where extra information will be recovered for citations.

{  
&nbsp;&nbsp;&nbsp;"metadata_prefix": "iso19139",  
&nbsp;&nbsp;&nbsp;"application": "EPOS",  
&nbsp;&nbsp;&nbsp;**"collect_extra_info_from_gfz"**:"http://dataservices.gfz-potsdam.de/getcitationinfo.php?doi=http://dx.doi.org/",  
&nbsp;&nbsp;&nbsp;"set":"~P3E9c3ViamVjdCUzQSUyMm11bHRpLXNjYWxlK2xhYm9yYXRvcmllcyUyMg"  
}

when 'collect extra info' is left out, there will be not retrieval for this information and a simple list of doi's will be presented.



*Email addresses for maintainers*   
Organisations (labs in CKAN) that will be used as maintainers, will have to have an email address as well.   
Within CKAN this can only be done by adding extra fields. It is not a standard field on organization level.  
Therefore use extra fields on organization level:

extras: [  
&nbsp;{  
  &nbsp;&nbsp;&nbsp;**value: "hdr@hdr.nl"**,  
  &nbsp;&nbsp;&nbsp;state: "active",  
  &nbsp;&nbsp;&nbsp;**key: "email"**,  
  &nbsp;&nbsp;&nbsp;revision_id: "b2356692-7f95-475e-88d3-1390451ccec7",  
  &nbsp;&nbsp;&nbsp;group_id: "7ad73491-aec5-4379-ae2c-44e03d05eaf4",  
  &nbsp;&nbsp;&nbsp;id: "2426a9b8-bfa3-4790-b5f9-f78d0d3eb2ee"  
&nbsp;}  
]



## Standard CKAN fields
**Standard CKAN fields**

-author  
Author of the package.  
-owner_org    
Organisation that owns the package and as such shown on the datapackage view  
-title  
Title of a package  
-notes  
Description of a package  
-license_id  
The license under which the datapackage can be used.  
-url  
URL referring to more detailed information regarding the datapackage  
-groups  
A datapackage can be linked to N groups.  
-tags  
A datapackage can be tagged to…  
-formats  
-maintainer  
Reference to where the CKAN package is maintained.  
-maintainer_email  
-extras
Key value pairs enabling a CKAN programmer to customise datapackage data to

**Extra fields for iLAB**:  
Locations covered  
Dataset contact  
Created at repository  
Year of publicatoin  
Publisher  
Collection period  

**Extra fields for EPOS**:  
Dataset contact  
Created at repo  
Publication date  
Publisher  
Is supplement to  
Cites  
References  
geobox-wLong  
geobox-eLong  
geobox-nLat  
geobox-sLat  

## CKANEXT-CUSTOM-THEMES
Mainly frontend items that transform standard CKAN into a tailored application. Eg. the iLAB catalog.  
This by overruling view files,  add static content like images and javascript.
