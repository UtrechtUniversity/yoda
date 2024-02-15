---
parent: Development
title: Running Yoda using Docker Compose
nav_order: 1
---
# Running Yoda using Docker Compose

Docker Compose configurations for running Yoda are available in the
`/docker` directory.

## Intended use and limitations

These configurations are intended for local development and testing.

Some components are not (yet) available in the containerized Yoda setup,
most importantly:
- OpenSearch (used for searching in the deposit module)
- The containerized version does not actually deliver emails sent by Yoda. 
  Instead, it has [Mailpit](https://github.com/axllent/mailpit) for testing email
  delivery. Mailpit provides a web interface that can be used to view email messages
  that would have been delivered by the application in a production configuration.
- The Docker Compose configurations only have an iRODS provider; there is no consumer
  for data replication.

## Prerequisites

Running the containerized Yoda setup requires Docker. The Yoda Docker Compose
configurations may not work on older versions of Docker / Docker Compose. Docker
20.10.x and newer is known to work.

For generic Docker installation instructions, see e.g.
[the Docker Engine installation docs]( https://docs.docker.com/engine/install/).
MacOS users can [install Colima and Docker](https://github.com/abiosoft/colima) using
[Homebrew](https://brew.sh).

## Starting the application

If you haven't downloaded the Docker images yet, pull them first:

```bash
cd docker/compose
docker-compose pull
```

Yoda has two Docker Compose configurations:
1. The regular configuration. This is the most portable and fastest configuration.
2. A configuration with bind mounts for the application source code. This configuration enables
   editing the Yoda source code without having to work in the container, so that you can use your
   host system IDE, editor, as well as other tools. However, bind mounts can be tricky to get working on
   some container runtimes / host operating systems, and they can slow down the application
   significantly in some setups.

In general, it is recommended to use the regular configuration, unless you need the bind mounts.

Start the regular configuration by running the start script in the `docker/compose` directory:

```bash
../up.sh
```

Start the configuration with bind mounts by running the start script in the `docker/compose-with-bind-mounts`
directory:

```bash
cd ../compose-with-bind-mounts
../up.sh
```

Removing and old instance of the application (including data):
```bash
../down.sh -v

# And in the configuration with bind mounts:
./clean.sh
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

## Jobs

Yoda uses jobs for various processes, such as creating revisions, archiving data in the vault, collecting
statistics data, and processing data package publication changes. These jobs need to be started manually
in the Docker Setup.

The `run-cronjob.sh` shell script can be used as a convenient way to start jobs.

For example, to asynchronously create revisions, run:

```
./run-cronjob.sh revision
```

After accepting a data package for archiving in the vault, run:

```
./run-cronjob.sh copytovault
```

After accepting a data package for publication, run:

```
./run-cronjob.sh publication
./run-cronjob.sh moaiupdate
```

If you want to view the statistics, first run the statistics job:

```
./run-cronjob.sh statistics
```

## Troubleshooting

### Cannot create container for service [...] : Conflict

The Docker setup currently has static container names so that we can easily
start jobs on containers, etc. This can however cause conflicts after, for example, the
container runtime has crashed.

If you don't have any other Docker containers running on your system, the easy way to
resolve such conflicts is to just stop and remove all containers:

```bash
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
```

### Error: bind mount owned by root user. Cannot change application UID

Multiple situations can cause failures when preparing to change the application UID to match the host system user:
1. One of the bind mount directories (`docker/compose-with-bind-mounts/v_*`) is owned by the root user, rather than a regular user.
   In this case: use `chown` to change ownership of this directory on the host system.
2. One of the bind mount directories (`docker/compose-with-bind-mounts/v_*`) is not present on the host system, which
   causes it to default to root permissions. In this case, the directory needs to be re-created with a `.docker.gitkeep` dummy file.
3. There is some kind of problem on the host system (e.g. SELinux denial, permission problem related to user mapping, etc.) that causes Docker
   to do something unexpected related to the bind mounts. Checking the host system logs for any clues could be a first step for troubleshooting
   in such a case.

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

### Yoda web mock

```bash
cd docker/images/yoda_web_mock
./build.sh
```
