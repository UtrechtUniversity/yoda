#!/usr/bin/env bash
#
# This script generates a certificate bundle for the Yoda Docker setup using OpenSSL.

set -e
set -x

openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -nodes -keyout docker.key -out docker.pem -config docker.cnf
openssl dhparam -out dhparam.pem 2048
tar cvfz docker-cert-bundle.tar.gz docker.pem docker.key dhparam.pem
