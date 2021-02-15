# Yoda technical documentation
On this website you can find release notes and technical documentation on administration tasks and software design of Yoda.

## What is this?
Yoda is a research data management solution developed by Utrecht University and used by multiple institutes around the world.
It provides researchers and their partners with a workspace and an archive that enables them to collaborate, deposit, publish and preserve research data.

## Release notes
- [release 1.7](release-notes/release-1.7.md) (TBA)
- [release 1.6](release-notes/release-1.6.md) (November 2020)
- [release 1.5](release-notes/release-1.5.md) (July 2019)
- [release 1.4](release-notes/release-1.4.md) (December 2018)
- [release 1.3](release-notes/release-1.3.md) (November 2018)
- [release 1.2](release-notes/release-1.2.md) (May 2018)
- [release 1.1](release-notes/release-1.1.md) (March 2018)
- [release 1.0](release-notes/release-1.0.md) (November 2017)
- [release 0.9.7](release-notes/release-0.9.7.md) (August 2017)

## Administration tasks
- [Configuring Yoda](administration/configuring-yoda.md)
- [Deploying Yoda](administration/deploying-yoda.md)
- [Applying a local change to a ruleset](administration/hotfixing-ruleset.md)
- [Installing licenses](administration/installing-licenses.md)
- [Installing terms](administration/installing-terms.md)
- [Installing preservable file formats](administration/installing-preservable-file-formats.md)
- [Installing metadata schemas](administration/installing-metadata-schemas.md)
- [Upgrading metadata schemas](administration/upgrading-metadata-schemas.md)
- [Background jobs](administration/background-jobs.md)
- [Troubleshooting publication](administration/troubleshooting-publication.md)
- [Restore collection](administration/restore-collection.md)
- [Configuring OpenId Connect](administration/configuring-openidc.md)

## Development
- [Setting up development environment](development/setting-up-development-environment.md)
- [Setting up YodaDrive development environment](development/yodadrive-development-environment.md)
- [Development environment test users and data](development/development-test-data.md)
- [Wall of Fame](development/wall-of-fame.md)

## Software design

### API
- [API documentation](https://petstore.swagger.io/?url=https://utrechtuniversity.github.io/irods-ruleset-uu/api.json)

### System
- [System overview](design/system-overview.md)
- [Research space](design/research-space.md)
- [Vault space](design/vault-space.md)
- [Statistics module](design/statistics.md)
- [Datarequests module](design/data-requests.md)
- [Group manager](design/group-manager.md)
- [External user service](design/external-user-service.md)
- [Yoda OAI-PMH endpoint](design/yoda-moai.md)

### Metadata
- [Metadata schema identifier](design/metadata-schema-identifier.md)
- [Metadata form](design/metadata-form.md)
- [Metadata mappings](design/metadata-mappings.md)
- [Metadata schemas](design/metadata-schemas.md)

### Processes
- [Asynchronous and privileged execution](design/async-system-execution.md)
- [Locking mechanism](design/locking-mechanism.md)
- [Publication process](design/publication-process.md)
- [Revision management](design/revisions.md)
- [Vault process](design/vault-process.md)

### Other
- [Python plugin](design/python-plugin.md)
- [Yoda drive](design/yodadrive.md)

## Documentation style
All documentation is styled using [Markdown](https://guides.github.com/features/mastering-markdown/).
All UML diagrams are generated with [PlantUML](http://plantuml.com/).

## License
This project is licensed under the GPLv3 license.

The full license can be found in [LICENSE](LICENSE).
