# Transformation of metadata within YoDa #

## Research area ##

**-yoda-metadata.xml**   
*yoda-metadata.xml* holds a **schemaLocation**.   
This designates the location of the publically accessible schema to which the data in yoda-metadata.xml must compy.

** research.xsd **   
Each YoDa-instance holds community based schemas internally for control of metadata integrity for that perticular community.
In such a system community folder reside:
- research.xsd   
The schema to which yoda-metadata.xml in the research area must comply
- vault.xsd   
The schema to which yoda-metadata.xml in the research area must comply

An example of configuration files for community 'iLab':

/tempZone/yoda/schemas/ilab/
- research.xsd
- vault.xsd
- All required xls's for the community

For the research area the file research.xsd determines the rules for yoda-metadata.xml.   
The **targetNamespace** within the xsd determines the ID / version.

Both schemaLocation in yoda-metadata.xml and targetNamespace in corresponding xsd must be equal.  
If not, transformation of data in yoda-metadata.xml must take place.


### Transformation of metadata ###
Transformation is mainly achieved by using a stylesheet (xls) to convert data from one schemaID to another.   

If using a stylesheet proves too difficult, or even impossible, the transformation software is set up as such that programmically (Python) changes can be performed as well.
Use of stylesheets is not a requirement for this purpose.

#### After transformation ####
After transformation of the metadata in yoda-metadata.xml the origin file is backed up like:   

yoda-metadata[5633743].xml

yoda-metadata.xml now holds the transformed data.   
And the schemaLocation is set to the correct schemaID.   
Thus safeguarding that no transformation will take place anymore.


## Code: ##


### Trap whether transformation is required###
PHP RESEARCH module: metadata.php-controller

*yoda-metadata.xml*  
**schemaLocation** is retrieved from xml => schemaID1

yoda-metadata.xml path delivers *category* (default or specific) and xsd space (research.xsd or vault.xsd)
**targetNamespace** is then retrieved from resulting xsd => schemaID2

If difference exists between schemaLocation (of the user's data) and targetNamespace of current xsd, schemaID1/schemaID2,  then transformation has to take place.

### Do transformation - within irods-ruleset-research ###
within iRods / iiSchemaUpdates.py:   
the tranformation matrix holds possible conversions from schemaIDn to schemaID(m)

    transformationMethod = transformationMatrix[schemaID1][schemaID2]

The matrix brings up a function name that will transform the data.
This can entail a scenario of steps to be taken. If possible simply by using a specific stylesheet.   
Sometimes more complicated actions have to take place.

Usage of stylesheets   
A stylesheet is used to transform xml data from 1 version to another.    
Within the stylesheet all structural and dynamic data can be collected and returned as a the new yoda-metadata.xml.   

*Namespaces required in stylesheet*   
The original metadata is using a specific namespace in which the data 'lives'.   
This has to be known in the transformation stylesheet as well. Otherwise, XPath queries will not result in any data!   

Secondly, the stylesheet describes the contents of the NEW yoda-metadata.xml which belong to its own new namespace.

Consequently, within a stylesheet both the new and old namespaces are required.

    <xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:yoda="https://utrechtuniversity.github.io/yoda-schemas/default"   
    exclude-result-prefixes="yoda">

      <xsl:template match="/">
        <xsl:apply-templates select="/yoda:metadata"/>
      </xsl:template>

      <xsl:template match="/yoda:metadata">
    <metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   
     xmlns="https://utrechtuniversity.github.io/yoda-schemas/default/v2"   
      xsi:schemaLocation="https://utrechtuniversity.github.io/yoda-schemas/default/v2 research.xsd">

This last row is what will become the <metadata> header row that is part of the new yoda-metadata.xml.
Thus defining its new default namespace and schemaLocation.
