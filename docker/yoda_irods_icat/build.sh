#!/bin/sh
export DOCKER_SCAN_SUGGEST=false
docker build . -t yodaprovider.azurecr.io/dev1.9
