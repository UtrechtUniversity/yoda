# Release notes Yoda version 1.0 (November 2017)

Version: 1.0

Released: November 2017

## What's new in Yoda version 1.0
### Features
- Researchers can submit a datapackage in the vault for publication after confirming the terms and agreements
- Datamanagers can approve the submit for publication
- The license text of a published datapackage is stored in the vault (license.txt)
- Datamanagers can update metadata of datapackages in the vault
- Anonymous users can view the landingpage of a published datapackage. The DOI (and link to the landingpage) is available on https://mds.datacite.org/
- Anonymous users can access 'open access' publications using the link on the landingpage. browser or webdav
- A subset of the metadata is published on https://mds.datacite.org/ , the landingpage and the moai server
- Harvesters can get the last modified date of the published record of a datapackage on the moai server
- Folders and datapackages have a provenance action log with historical information of the actions, the user that initiated the action with date and time
- Published datapackages in the vault provide system metadata with package size, doi, landingpage uri
- Metadata supports hierarchical constructs, replication of fields and constructs, compound fields (when filled all fields have to be filled)
- Datapackages in the vault have different statuses, search for status has been extended accordingly
- All regular users of a research group have read access, by default, to the group's datapackages in the vault. The datamanager can revoke group access.
- Searching is no longer case sensitive
- All members of a group can view the groups storage consumption and trends using the statistics module

## Upgrading from 0.9.7
Upgrade is supported by Ansible (2.4.x). No migrations required.

- yoda-metadata.xsd is changed. Existing 0.9.7 metadata is not supported and needs to be updated manually
- publication functionality requires a datamanager group and datamanager user for a category and the datamanager group folder must exist
- Ansible can be used for deployment and updates
- terms and agreement text files (html) have to be installed by the administrator. The most recent file will be used
- license files (e.g. CC-BY.txt), with the license text and uri files (e.g. "https://creativecommons.org/licenses/by/4.0/legalcode" have to be installed by the administrator
- default XSD, schema-for-formelements.xsd, schema-for-xsd.xsd, XML, default.xsl, default2landingpage.xsl and default2datacite.xsl have to be installed by the administrator

## Known Issues
- when the datamanager saves updated metadata in the vault, the portal shows the old metadata. Saving the changes in the vault takes at most 1 minute. Close and re-open the metadata to see if your changes are shown, before taking further actions (e.g. approve for publication)
- The iRODS server will get slower over time due to a memory leak. A workaround is suggested above in the upgrade section. iRODS 4.1.11 (included is Yoda 1.0) may have solved this problem.
- When storage data is available, different tiers are assigned, and all resources are then reset to the same tier, the statistics module may show a blank page
- Ordering of data in tables is not working. Clicking column sort headers have been disabled and are not shown.
