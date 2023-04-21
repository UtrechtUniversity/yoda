#!/bin/sh
export DOCKER_SCAN_SUGGEST=false
docker build . -t ghcr.io/utrechtuniversity/yoda-portal:dev-1.9
