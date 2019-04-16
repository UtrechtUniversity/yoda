# WHAT HIERMEE TE DOEN???

## Submit to vault
When requesting a datapackage to be accepted into the vault, its corresponding metadata will be validated first.
Validation will take place against the community XSD. If this does not exists, validation will take place against the default XSD of the YoDa instance.

![OVerview MOAI-CKAN](img/to_vault.png)

The XSD is a transformation of the JSON schema's that are maintained by the YoDa development team.
The Yoda team wrote a program to be able to do so.
The documentation of this conversion tool can be found here:



### Processing of posted metadata in the vault workspace by the datamanager
The metadata form is also used for editing of metadata when the data package has already been accepted and copied to the vault.

A datamanager, a yoda-user that is member of a datamanager-group for the same research-group, can still edit metadata for the package that is already in the vault.
However, the data as originally entered by the researcher and accepted for the vault by a datamanager is never compromised / lost.

The presented metadata form within the vault uses the same technique as in the dynamic storage space.
Difference is that the newly added data is not actually overwriting the data in yoda-metadata.xml.
The metadata form saves ithe older data in the vault in the corresponding folder but always with a unique name, based upon timestamps.
Thus safeguarding earlier or original metadata.
