#!/bin/sh
export DOCKER_SCAN_SUGGEST=false
docker build . -t yodaeus.azurecr.io/dev-1.9
