# KAN DIT ERGENS ANDERS NOG BIJ???

## Community dependency
Within YoDa, research is supported via groups;  administrative entities declaring which persons are allowed to participate in that perticular research.

Each group within YoDa belongs to a community. A community (=category ) can hold multiple groups.

YoDa is designed in such a way that each community can have its own metadata definition.
If such definition is not present, a YoDa instance is always equipped with a default definition.
The metadata definition is declared in JSON schema’s.

A metadata definition should always include all information that is required to be able to publish the research datapackage, including its metadata.
The exact fields can be found on datacite.org

Community dependent files are stored on the virtual iRods drive:

**/tempZone/yoda/schemas**

Each subfolder designates an area that corresponds to a category.

So,
**/tempZone/yoda/schemas/ilab**

holds all the required files for category ilab.

Always, also included is:

**/tempZone/yoda/schemas/default**

Which is the area which holds the default required files where categories do not have its designated category area.

WIthin a category folders following files are located:

- metadata.JSON
The JSON schema for the category.
- research.XSD
results from metadata.JSON but without mandatoryness included
- vault.XSD
results from metadata.JSON but with mandatoryness included
