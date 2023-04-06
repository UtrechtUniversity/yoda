#!/bin/bash

function before_update {
  echo -e "[...] ${1}"
}

function progress_update {
  GREEN='\033[0;32m'
  RESET='\033[0m'
  echo -e "[ ${GREEN}\xE2\x9C\x94${RESET} ] ${1}"
}

# Download test vault and iCAT data
before_update "Downloading vault and iCAT test data"
mkdir /download
wget -q https://yoda.uu.nl/yoda-docker/dev-1.9.vault.tar.gz -O /download/dev-1.9.vault.tar.gz
progress_update "Downloaded vault test data."
wget -q https://yoda.uu.nl/yoda-docker/dev-1.9.icat.sql.gz -O /download/dev-1.9.icat.sql.gz
progress_update "Downloaded iCAT test data."

# Extract vault test data
cd /var/lib/irods
sudo -iu irods tar xfz /download/dev-1.9.vault.tar.gz

# Wait for database container to become available
before_update "Waiting for PostgreSQL container to come up ..."
while ! nc -z db.yoda 5432; do
  printf "."
  sleep 0.5
done
progress_update "PostgreSQL is now up."

# Load iCAT test data
export PGPASSWORD=yodadev
gunzip -c /download/dev-1.9.icat.sql.gz | psql -U irodsdb -d ICAT -h db.yoda -p 5432

# ...
sleep infinity
