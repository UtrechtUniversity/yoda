#!/bin/sh

set -e
set -u
set -x

export MAILPIT_VERSION=1.17.0
export DOCKER_SCAN_SUGGEST=false
DOCKER_TAG="$1"

if [ -z "$DOCKER_TAG" ]
then echo "Error: no docker tag argument provided."
     exit 1
else shift
fi

if [ -d "mailpit" ]
then rm -rf mailpit
fi

git clone https://github.com/axllent/mailpit.git
cd mailpit
git checkout "v$MAILPIT_VERSION"
docker build . -t "ghcr.io/utrechtuniversity/yoda-mailpit:$DOCKER_TAG" --build-arg VERSION="$MAILPIT_VERSION" "$@"
