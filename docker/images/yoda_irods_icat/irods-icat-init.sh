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
  before_update "Starting iRODS"
  sudo -u irods /var/lib/irods/irodsctl start || true
  progress_update "iRODS started"

  before_update "Initializing authentication token"
  sudo -u irods bash -c "echo rods | iinit"
  progress_update "Authentication token initialized"

  progress_update "Container startup complete. iRODS is running."

  sleep infinity
}

if [ -f "/container_initialized" ]
then echo "Container has already been initialized. Starting service."
     start_service
fi

# Download test vault and iCAT data
before_update "Downloading data"
mkdir /download
wget -q "https://yoda.uu.nl/yoda-docker/${DATA_VERSION}.vault.tar.gz" -O "/download/${DATA_VERSION}.vault.tar.gz"
progress_update "Downloaded vault test data."
wget -q "https://yoda.uu.nl/yoda-docker/${DATA_VERSION}.icat.sql.gz" -O "/download/${DATA_VERSION}.icat.sql.gz"
progress_update "Downloaded iCAT test data."
wget -q "https://yoda.uu.nl/yoda-docker/${DATA_VERSION}.certbundle.tar.gz" -O "/download/${DATA_VERSION}.certbundle.tar.gz"
progress_update "Downloaded certificate bundle."

# Extract vault test data
before_update "Extracting vault data"
cd /var/lib/irods
sudo -iu irods tar xfz "/download/${DATA_VERSION}.vault.tar.gz"
progress_update "Vault data extracted"

# Extract certificate bundle
before_update "Extracting certificate data"
cd /download
tar xvfz "$DATA_VERSION.certbundle.tar.gz"
install -m 0644 -o irods -g irods docker.pem /etc/irods/localhost_and_chain.crt
install -m 0644 -o irods -g irods docker.key /etc/irods/localhost.key
install -m 0644 -o irods -g irods dhparam.pem /etc/irods/dhparams.pem
progress_update "Certificate data extracted"

# Wait for database container to become available
before_update "Waiting for PostgreSQL container to come up ..."
export PGPASSWORD=yodadev
while ! psql -U irodsdb -d ICAT -h db.yoda -p 5432 -c 'SELECT 1' >& /dev/null ; do
  printf "."
  sleep 0.5
done
progress_update "PostgreSQL is now up."

# Load iCAT test data
before_update "Loading iCAT database data"
export PGPASSWORD=yodadev
gunzip -c "/download/${DATA_VERSION}.icat.sql.gz" | psql -U irodsdb -d ICAT -h db.yoda -p 5432
progress_update "iCAT database data loaded"

INSTALL_TIMESTAMP=$(date +'%Y-%m-%dT%H:%M:%S.000000')
cat > /var/lib/irods/VERSION.json << VERSION
{
    "catalog_schema_version": 8, 
    "commit_id": "bc6f9f1cdef6c4ec01ea14402428988892615321", 
    "configuration_schema_version": 3, 
    "installation_time": "$INSTALL_TIMESTAMP", 
    "irods_version": "4.2.11"
}
VERSION
chown irods:irods /var/lib/irods/VERSION.json

CURRENT_UID="$(id -u irods)"
if [[ -f "/etc/irods/yoda-ruleset/.docker.gitkeep" ]]
then progress_update "Bind mount detected. Checking if application UID needs to be changed."
     MOUNT_UID="$(stat -c "%u" /etc/irods/yoda-ruleset)"
     if [ "$MOUNT_UID" == "0" ]
     then progress_update "Error: bind mount owned by root user. Cannot change application UID. Halting."
          sleep infinity
     elif [ "$MOUNT_UID" == "$CURRENT_UID" ]
     then progress_update "Notice: bind mount UID matches application UID. No need to change application UID."
     else before_update "Updating application UID ${CURRENT_UID} -> ${MOUNT_UID}"
          usermod -u "$MOUNT_UID" irods
          find / -xdev -user "$CURRENT_UID" -exec chown -h "${MOUNT_UID}" {} \;
          progress_update "Application UID updated."
     fi
     if [ -d "/etc/irods/yoda-ruleset/.git" ]
     then echo "Git repo detected in bind mount. Skipping code copy in order not to overwrite local changes."
     else
         before_update "Fixing up permissions before copying application source code."
         find /etc/irods/yoda-ruleset-copy -type f -perm 0444 -exec chmod 0666 {} \;
         progress_update "Permission fixes done."
         before_update "Copying ruleset code to volume."
         cp -R /etc/irods/yoda-ruleset-copy/. /etc/irods/yoda-ruleset
         progress_update "Copying ruleset source code finished."
     fi
else progress_update "Notice: no bind mount detected. Keeping current application UID ${CURRENT_UID}"
fi

before_update "Creating DAP token database"
sudo -iu irods /etc/irods/yoda-ruleset/tools/setup_tokens.sh /etc/irods/yoda-ruleset/accesstokens.db test
progress_update "Creating DAP token database"

before_update "Building ruleset"
cd /etc/irods
ln -s yoda-ruleset rules_uu
cd yoda-ruleset
make install
progress_update "Ruleset updated"

before_update "Updating ruleset dependencies"
sudo -u irods pip2 install --user attrs==21.4.0
sudo -u irods pip2 install --user -r /etc/irods/yoda-ruleset/requirements.txt
progress_update "Ruleset dependencies updated"

touch /container_initialized
start_service
