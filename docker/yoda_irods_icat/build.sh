#!/bin/sh
export DOCKER_SCAN_SUGGEST=false
docker build . -t ghcr.io/utrechtuniversity/yoda-provider:dev-1.9 "$@"
