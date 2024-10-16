#!/bin/bash

set -e
set -o pipefail
set -u

DATA_VERSION="$1"

if [ -z "$DATA_VERSION" ]
then echo "Error: no data version argument provided."
     exit 1
fi

function before_update {
  echo -e "[...] ${1}"
}

function progress_update {
  GREEN='\033[0;32m'
  RESET='\033[0m'
  echo -e "[ ${GREEN}\xE2\x9C\x94${RESET} ] ${1}"
}

function start_service {
  apache2ctl -D FOREGROUND || true
  echo "Error: Apache either terminated or would not start. Keeping container running for troubleshooting purposes."
  sleep infinity
}

if [ -f "/container_initialized" ]
then echo "Container has already been initialized. Starting service."
     start_service
fi

# Download and install certificates
before_update "Downloading certificate bundle"
wget -q "https://yoda.uu.nl/yoda-docker/${DATA_VERSION}.certbundle.tar.gz" -O "/download/${DATA_VERSION}.certbundle.tar.gz"
progress_update "Downloaded certificate bundle."

# Extract certificate bundle
before_update "Extracting certificate data"
cd /download
tar xvfz "${DATA_VERSION}.certbundle.tar.gz"
install -m 0644 docker.pem /etc/ssl/certs/localhost.crt
install -m 0644 docker.pem /etc/ssl/certs/localhost_and_chain.crt
install -m 0644 docker.key /etc/ssl/private/localhost.key
install -m 0644 dhparam.pem /etc/ssl/private/dhparams.pem
progress_update "Certificate data extracted"

# Start Apache
touch /container_initialized
before_update "Initialization complete. Starting Apache"
start_service
