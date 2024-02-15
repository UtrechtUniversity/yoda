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

function start_service {
  /usr/sbin/httpd -DFOREGROUND || true
  echo "Error: http either terminated or would not start. Keeping container running for troubleshooting purposes."
  sleep infinity
}

if [ -f "/container_initialized" ]
then echo "Container has already been initialized. Starting service."
     start_service
fi

# Download and install certificates
before_update "Downloading certificate bundle"
mkdir /download
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

# Update permissions / UID for bind mount, if needed
CURRENT_UID="$(id -u yodadeployment)"
if  [[ -f "/var/www/moai/yoda-moai/.docker.gitkeep" ]]
then progress_update "Bind mount detected. Checking if application UID needs to be changed."
     MOUNT_UID="$(stat -c "%u" /var/www/moai/yoda-moai)"
     if [ "$MOUNT_UID" == "0" ]
     then progress_update "Error: bind mount owned by root user. Cannot change application UID. Halting."
          sleep infinity
     elif [ "$MOUNT_UID" == "$CURRENT_UID" ]
     then progress_update "Notice: bind mount UID matches application UID. No need to change application UID."
     else before_update "Updating application UID ${CURRENT_UID} -> ${MOUNT_UID}"
          usermod -u "$MOUNT_UID" yodadeployment
          find / -xdev -user "$CURRENT_UID" -exec chown -h "${MOUNT_UID}" {} \;
          progress_update "Application UID updated."
     fi
     if [[ -d "/var/www/moai/yoda-moai/.git" ]]
     then echo "Git repo detected in bind mounts. Skipping code copy in order not to overwrite local changes."
     else
         before_update "Fixing up permissions before copying application source code."
         find /var/www/moai/yoda-moai-copy -type f -perm 0444 -exec chmod 0666 {} \;
         progress_update "Permission fixes done."
         before_update "Copying application source code to volume."
         cp -Ru /var/www/moai/yoda-moai-copy/. /var/www/moai/yoda-moai
         progress_update "Copying application source code finished."
     fi
else progress_update "Notice: no bind mount detected. Keeping current application UID ${CURRENT_UID}"
fi

# Restore landing page files to volume if needed
if ! [[ -f "/var/www/landingpages/index.html" ]]
then before_update "Copying back landing page core contents to volume."
     cp -Ru /var/www/landingpages-copy/. /var/www/landingpages
     progress_update "Copying landing page core contents finished."
fi

# Initialize MOAI
before_update "Initializing MOAI database."
sudo -iu yodadeployment /var/www/moai/yoda-moai/venv/bin/update_moai --config /var/www/moai/settings.ini yoda_moai
progress_update "MOAI database initialized."

# Start Apache
touch /container_initialized
before_update "Initialization complete. Starting Apache"
start_service
