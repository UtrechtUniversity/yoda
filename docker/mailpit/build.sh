#!/bin/sh

set -e
set -u
set -x

export DOCKER_SCAN_SUGGEST=false

if [ -d "mailpit" ]
then rm -rf mailpit
fi

git clone https://github.com/axllent/mailpit.git
cd mailpit
git checkout v1.5.0
docker build . -t ghcr.io/utrechtuniversity/yoda-mailpit:dev-1.9
