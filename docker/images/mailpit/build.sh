#!/bin/sh

set -e
set -u
set -x

export MAILPIT_VERSION=1.9.4
export DOCKER_SCAN_SUGGEST=false

if [ -d "mailpit" ]
then rm -rf mailpit
fi

git clone https://github.com/axllent/mailpit.git
cd mailpit
git checkout "v$MAILPIT_VERSION"
docker build . -t ghcr.io/utrechtuniversity/yoda-mailpit:dev-1.9 --build-arg VERSION="$MAILPIT_VERSION" "$@"
