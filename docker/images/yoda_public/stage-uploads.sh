#!/bin/bash
#
# This script stages static files for the Yoda public host by copying
# them from the Ansible playbook. This should run before run the Dockerfile
# to create the image

set -e
set -o pipefail
set -x

cd "$(dirname "$0")"

if ! [ -d ./stage ]
then mkdir ./stage
fi

cp ../../../roles/yoda_landingpages/files/index.html stage
cp ../../../roles/yoda_landingpages/files/css/bootstrap.min.css stage
cp ../../../roles/yoda_landingpages/files/css/uu.css stage
cp ../../../roles/yoda_landingpages/files/img/logo.svg stage
cp ../../../roles/yoda_landingpages/files/img/logo_footer.svg stage
cp ../../../roles/yoda_landingpages/files/css/leaflet-1.5.1.css stage
cp ../../../roles/yoda_landingpages/files/js/leaflet-1.5.1.js stage
