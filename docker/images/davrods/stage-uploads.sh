#!/bin/bash
#
# This script stages static files for the Yoda iCAT container by copying
# them from the Ansible playbook. This should run before run the Dockerfile
# to create the image

set -e
set -o pipefail
set -x

cd "$(dirname "$0")"

if ! [ -d ./stage ]
then mkdir ./stage
fi

cp ../../../roles/yoda_davrods/files/initialize-davrods-lockdb.py stage
