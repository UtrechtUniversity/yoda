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
while ! nc -z db.yoda 5432; do
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

before_update "Starting iRODS"
sudo -u irods /var/lib/irods/irodsctl start || true
progress_update "iRODS started"

before_update "Initializing authentication token"
sudo -u irods bash -c "echo rods | iinit"
before_update "Authentication token initialized"

sleep infinity
