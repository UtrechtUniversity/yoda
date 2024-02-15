#!/bin/bash

# This script takes care of copying landing page and metadata files
# to the public host. This versions is meant for the Docker setup,
# and uses shared volumes (rather than scp, as the script name suggests) to
# copy files to the public server
set -e
set -x

PHYPATH=$1
HOST=$2
USER=$3
DESTINATION=$4
DESTDIR=$(dirname $DESTINATION)

mkdir -p "/public/$DESTDIR"
cp "$PHYPATH" "/public/$DESTINATION"
chmod go+r "/public/$DESTINATION"
