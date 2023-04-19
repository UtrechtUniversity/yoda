#!/bin/sh
export DOCKER_SCAN_SUGGEST=false
docker build . -t davrods.azurecr.io/dev-1.9
