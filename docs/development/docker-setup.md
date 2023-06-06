---
parent: Development
title: Running Yoda using Docker Compose
nav_order: 1
---
# Running Yoda using Docker Compose

A Docker Compose configuration for running Yoda is available in the
`/docker` directory.

## Intended use and limitations

The configuration is intended for local development and testing.

Some components are not yet available in the containerized version of Yoda,
most importantly:
- The public server (landing pages and OAI-PMH). This also implies that publication
  functions are not yet available.
- OpenSearch (used for searching in the deposit module)
- The configuration uses Mailpit for testing email delivery. Email delivery using
  Postfix is not yet available.
- The Docker Compose configuration has only the iRODS provider, there is no consumer
  for replication.

The cronjobs for revision creation, revision cleanup, archiving vault data etc. do not
run automatically, but need to be started manually in this configuration. The `run-cronjob.sh`
shell script can be used as a quick way to start the most commonly used cronjobs, e.g.:

```
run-cronjob.sh revision
```

## Starting the application

If you haven't downloaded the Docker images yet, pull them first:

```bash
cd docker/compose
docker-compose pull
```

The application can then be started using docker compose:
```bash
./up.sh
```

The default Docker Compose configuration uses bind mounts so that the ruleset, portal
and EUS application code can be edited easily. If that does not work on your system, there
is an alternative Docker Compose configuration without these volumes in `docker/compose-without-volumes`
that facilitates testing Yoda in situations where bind mounts cause problems.

Removing and old instance of the application (including data):
```bash
./down.sh -v
```

You need to have these entries in your /etc/hosts (or equivalent) file:

```
# Docker setup Yoda
127.0.0.1 portal.yoda eus.yoda data.yoda public.yoda
```

After the application is started, the web interfaces will be available on:
- Mailpit: http://localhost:8025
- Portal: https://portal.yoda:8443
- EUS (port with API enabled): https://eus.yoda:8444
- DavRODS: https://data.yoda:8445
- Public: https://public.yoda:8446

You can log in on the Yoda portal using any of the test account credentials, such as user name `researcher`
and password `test`. A full list of test account credentials can be found in the
[test_users list in the defaults file of the Yoda test role](https://github.com/UtrechtUniversity/yoda/blob/development/roles/yoda_test/defaults/main.yml).

## Building the images

Building a new image is only needed for development purposes. If you want to test
an existing Dockerized version of Yoda, you can pull the images from the registry
instead.

### Yoda provider

```bash
cd docker/images/yoda_irods_icat
./stage-uploads.sh
./build.sh
```

### Mailpit

```bash
cd docker/images/mailpit
./build.sh
```

### Yoda portal

```bash
cd docker/images/yoda_portal
./build.sh
```

### DavRODS

```bash
cd docker/images/davrods
./build.sh
```

### External user service

```bash
cd docker/images/yoda_eus
./build.sh
```

### Public

```bash
cd docker/images/yoda_public
./stage-uploads.sh
./build.sh
```
