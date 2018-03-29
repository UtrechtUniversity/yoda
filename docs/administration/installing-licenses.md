# Installing Licenses
If the metadata Schema includes a License as a list of values it is possible to automatically add a License text and URI
to a package put in the vault. For every value of this field the copy to vault process will check if a
/rodsZone/yoda/licenses/${LICENSE}.txt exists. This file will be copied to a License.txt in the root of the vault
package. In the same collection a {License}.uri will be read and put in iRODS metadata, so it can be used for
publication. To prevent whitespace to enter the URI, the URI needs to be quoted by double quotes. The {License}.txt
needs to be pure ASCII to assure it will be displayed correctly on every Operating System on all browsers and the web
disk. UTF-8 is not an option because browsers will display a .txt file wih the windows-1252 encoding. The ANSI subset of
the windows-1252 encoding is not an option, because MAC and linux will not correctly detect ANSI in a .txt file if opened
from the web disk. In irods-ruleset-research/tools/licenses you will find three licenses with URIs as an example. To put
these into iRODS the first time do the following:

```bash
iput -r /etc/irods/irods-ruleset-research/tools/licenses /${RODSZONE}/yoda
```

To add extra licenses you will need to upload the .txt and .uri seperately. Replace ${LICENSE} with the name of the license
as it is defined in the XSD and ${RODSZONE} with the name of the iRODS zone.

```bash
iput "${LICENSE}.txt" "/${RODSZONE}/yoda/licenses/${LICENSE}.txt"
iput "${LICENSE}.uri" "/${RODSZONE}/yoda/licenses/${LICENSE}.uri"
```
