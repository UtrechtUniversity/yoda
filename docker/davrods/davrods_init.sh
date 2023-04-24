#!/bin/bash

set -e
set -o pipefail
set -u

DATA_VERSION="dev-1.9"

function before_update {
  echo -e "[...] ${1}"
}

function progress_update {
  GREEN='\033[0;32m'
  RESET='\033[0m'
  echo -e "[ ${GREEN}\xE2\x9C\x94${RESET} ] ${1}"
}

# Download and install certificates
before_update "Downloading certificate bundle"
wget -q "https://yoda.uu.nl/yoda-docker/${DATA_VERSION}.certbundle.tar.gz" -O "/download/${DATA_VERSION}.certbundle.tar.gz"
progress_update "Downloaded certificate bundle."

# Extract certificate bundle
before_update "Extracting certificate data"
cd /download
tar xvfz "${DATA_VERSION}.certbundle.tar.gz"
install -m 0644 docker.pem /etc/pki/tls/certs/localhost.crt
install -m 0644 docker.pem /etc/pki/tls/certs/localhost_and_chain.crt
install -m 0644 docker.key /etc/pki/tls/private/localhost.key
install -m 0644 dhparam.pem /etc/pki/tls/private/dhparams.pem
progress_update "Certificate data extracted"

# Start Apache
before_update "Initialization complete. Starting Apache"
/usr/sbin/httpd -DFOREGROUND || true
echo "Error: http either terminated or would not start. Keeping container running for troubleshooting purposes."
sleep infinity
