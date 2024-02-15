#!/usr/bin/env bash
#
# This script generates a certificate bundle for the Yoda Docker setup using OpenSSL.

set -e
set -x

openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes -keyout docker.key -out docker.pem -config docker.cnf

if [ -f "dhparam.pem" ]
then echo "Skipping DHParam generation, because DHParam file is already present."
else openssl dhparam -dsaparam -out dhparam.pem 4096
fi

tar cvfz docker-cert-bundle.tar.gz docker.pem docker.key dhparam.pem
