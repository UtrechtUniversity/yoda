---
layout: default
title: Running Yoda using Docker Compose
nav_order: 5
has_children: false
has_toc: false
---
# Running Yoda using Docker Compose

A Docker Compose configuration for running Yoda is available in the
`/docker` directory.

## Intended use and limitations

The configuration is intended for local development and testing.

Some components are not yet available in the containerized version of Yoda,
most importantly:
- The public server (landing pages and OAI-PMH). This also means the publication
  functions are not yet available.
- OpenSearch (used for searching in the deposit module)
- The configuration uses Mailpit for testing email delivery. Email delivery using
  Postfix is not yet available.
- The Docker Compose configuration has only the iRODS provider, there is no consumer
  for replication.

The cronjobs for revision creation, revision cleanup, archiving vault data etc. do not
run automatically, but need to be started manually in this configuration.

## Building the images

The iRODS provider image:

```bash
cd docker/yoda_irods_icat
./stage-uploads.sh
./build.sh
```

The Mailpit image:

```bash
cd docker/mailpit
./build.sh
```

The portal image:

```bash
cd docker/yoda_portal
./build.sh
```

## Starting the application

The application can be started using docker compose:
```bash
docker-compose up
```

Removing and old instance of the application:
```bash
docker-compose down -v
```

You need to have these entries in your /etc/hosts (or equivalent) file:

```
# Docker setup Yoda
127.0.0.1 portal.yoda eus.yoda data.yoda
```

After the application is started, the web interfaces will be available on:
- Mailpit: http://localhost:8025
- Portal: https://portal.yoda:8443
- EUS (port with API enabled): https://eus.yoda:8444
- DavRODS: https://data.yoda:8445
