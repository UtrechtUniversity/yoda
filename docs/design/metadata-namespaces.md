# Namespaces within Yoda

## XML standards for yoda-metadata.xml
To comply with xml standards, yoda-metadata.xml is equipped with a default namespace.
Furthermore, yoda-metadata.xml is extended with the reference of its schemalocation.   
I.e. the location of the its validation schema.
This, so any user knows to what schema the data is validated.

This validation schema is dependent on the space within Yoda, research or vault.
In the example below, the data within yoda-metadata.xml lives in research area and will be validated agains research.xsd.

The schemas are publically accessible and stored in Github.
```
<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   
 xmlns="https://yoda.uu.nl/schemas/default-0"   
 xsi:schemaLocation="https://yoda.uu.nl/schemas/default-0 research.xsd">
  <Title>1</Title>
  <Description>2</Description>
  <Version>3</Version>
  <Language>en - English</Language>
  <Retention_Period>10</Retention_Period>
  <Data_Classification>Public</Data_Classification>
  <Creator>
    <Name>bla</Name>
    <Properties>
      <Affiliation>Utrecht University</Affiliation>
      <Person_Identifier>
        <Name_Identifier_Scheme>ORCID</Name_Identifier_Scheme>
        <Name_Identifier>ad</Name_Identifier>
      </Person_Identifier>
    </Properties>
  </Creator>
  <License>Creative Commons Attribution 4.0 International Public License</License>
  <Data_Access_Restriction>Restricted - available upon request</Data_Access_Restriction>
</metadata>
```

## Using XSL with yoda-metadata.xml

Given that yoda-metadata.xml lives within a certain namespace, to be able to retrieve data from it when using XPath statements, a corresponding namespace must be added to the stylesheet.
```
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:yoda="https://yoda.uu.nl/schemas/default-0"
    exclude-result-prefixes="yoda">

  <xsl:template match="/">
        <xsl:apply-templates select="/yoda:metadata"/>
  </xsl:template>
```

Above the namespace alias 'yoda' (xmlns:yoda="https://yoda.uu.nl/schemas/default-0") makes sure that, if both namespaces are equal, XPath selection actually retrieves data.
