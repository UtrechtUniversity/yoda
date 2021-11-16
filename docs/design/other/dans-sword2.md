---
grand_parent: Software design
parent: Other
---
# DANS sword2.0 interface
## Description
The interface uses a bag holding all data and corresponding metadata of research to be deposited at DANS.  
See below for description of a 'bag'.

The bag is posted to DANS using a SWORD-client.
Yoda uses: https://github.com/swordapp/python-client-sword2/wiki/Quickstart

After posting, a response is received holding a URL that must be used in order to receive that processing status of the deposit process.

## 'statement' URI
https://act.easy.dans.knaw.nl/sword2/statement/09af7269-2b77-458d-99c2-651be6fb3435  

This URI is received when depositing.
The response holds the reference to the processing status of the deposit.


## Statuses
DRAFT – a bag can be sent in multiple phases (continued deposit) and this is the state when the last part is not received yet  
SUBMITTED – deposit is in queue to be processed  
INVALID – bag that was sent is not valid (technically).   
REJECTED – bag that was sent is not according to rules set by DANS
FAILED – technical error by DANS  
ARCHIVED – deposit is complete and accepted. The data is archived


## Process statuses and DOI
Het is de bedoeling dat jullie af en toe de statement URL aanroepen om te kijken wat de status van de deposit is. Is die **SUBMITTED**, probeer het dan later nog eens (wanneer het druk is, kan de wachtrij soms behoorlijk oplopen waardoor het langer duurt om de data te verwerken). Wanneer deze **ARCHIVED** is, ben je klaar.  
Eventueel haal je dan nog wat informatie uit de XML, zoals de URL naar EASY (body van <category>) of de **DOI** (href attribute in <link>).

## Error statuses
Wanneer je **INVALID of REJECTED** tegenkomt, hebben jullie zelf iets fout gedaan.
Over het algemeen proberen we deze foutmeldingen zo duidelijk mogelijk op te schrijven, maar als je iets tegen komt wat niet duidelijk is, dan horen we dat natuurlijk graag!
Bij een **FAILED** deposit is er aan onze kant iets niet goed gegaan. Dit kan bijv. een omgevallen service of een bug in de applicatie zijn. We proberen deze uiteraard z.s.m. op te losse




## Bag description

A bag must contain the following items:  
package name  
&nbsp;&nbsp;/data  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  .. actual data package data  
&nbsp;&nbsp;/metadata  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dataset.xml  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;files.xml - declaration of files in /data folder
&nbsp;&nbsp;bag-info.txt  
&nbsp;&nbsp;bagit.txt  
&nbsp;&nbsp;manifest-sha1.txt  
&nbsp;&nbsp;tagmanifest-md5.txt  


#### bag-info.txt
Payload-Oxum: 3212743.5  
Bagging-Date: 2018-04-13  
Bag-Size: 3.1 MB  
Created: 2016-11-12T23:41:11.000+00:00

#### bagit.txt
BagIt-Version: 0.97  
Tag-File-Character-Encoding: UTF-8

#### manifest-sha1.txt
Describes all files in data folder including each sha1.

f50380cd3a4ae5b8ea3d524a4b1e8582eca50893  data/README.md  
0a66ea77834e337e28a043db6d6f3d745c944593  data/random-images/image03.jpeg  
f100629544e98ad21503b04a276fe6185cb4e9d2  data/random-images/image01.png  
f750a66151421a62521be6495684fb8384cb4aa0  data/a/deeper/path/With-some-file.txt  
4ae4fb20ee161b8026a468160553e623dcea4914  data/random-images/image02.jpeg

#### tagmanifest-md5.txt
0162e3bed9af9459d68241cf235281b8 &nbsp;&nbsp; bag-info.txt  
9e5ad981e0d29adc278f6a294b8c2aca &nbsp;&nbsp; bagit.txt  
e5811f26340bf1a74a866c9f4825384e &nbsp;&nbsp; metadata/dataset.xml  
8beffb1f328ff9227f1f862ecb1ff4e6 &nbsp;&nbsp; metadata/files.xml  
1ee7172e6a9991bde1e7d381f37e7747 &nbsp;&nbsp; manifest-sha1.txt



Code example (just testing possibilities - to be elaborated):
```
from sword2 import Connection

SD_URI = 'https://act.easy.dans.knaw.nl/sword2/collection/1'

from sword2 import sword2_logging

print('hallo')
c = Connection(SD_URI, user_name = "yodatest", user_pass="y$6]AQ5$BZ\Z")


print('hallo-1')

# upload "package.zip" to this collection as a new (binary) resource:
with open("package.zip", "r") as pkg:
    print('hallo-2')
    receipt = c.create(col_iri = SD_URI,
                                payload = pkg,
                                mimetype = "application/zip",
                                filename = "package.zip",
                                packaging = 'http://purl.org/net/sword/package/Binary',
                                in_progress = False)    # As the deposit isn't yet finished
    print('++++++++++++++++++++++++++')
    print(receipt)

    print('se iri=' + receipt.se_iri)
    print('media iri=' + receipt.edit_media)

    print('edit iri=' + receipt.edit)

    print('##################')
    print(receipt.links)

    print('#########')
    print(receipt.links['http://purl.org/net/sword/terms/statement'][0]['href'])
    statementURI = receipt.links['http://purl.org/net/sword/terms/statement'][0]['href']

    #print(receipt.content)

    print('**************************')


    c2 = Connection(statementURI, user_name = "yodatest", user_pass="y$6]AQ5$BZ\Z")
    resp = c2.get_resource(statementURI)
    print(resp)

    print(':::::::::::::::::::::::::')
    print(resp.response_headers)
    print(':::::::::::::::::::::::::')
    print(resp.content)
    print(':::::::::::::::::::::::::')
    print(resp.code)


    print('--------------------------')


exit()
```
