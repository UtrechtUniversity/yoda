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

CURRENT_UID="$(id -u yodadeployment)"
if  [[ -f "/var/www/yoda/.docker.gitkeep" || -f "/var/www/extuser/.docker.gitkeep" ]]
then progress_update "Bind mount detected. Checking if application UID needs to be changed."
     MOUNT_UID="$(stat -c "%u" /var/www/yoda)"
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
     if [[ -d "/var/www/yoda/.git" || -d "/var/www/extuser/yoda-external-user-service/.git" ]]
     then echo "Git repo detected in bind mounts. Skipping code copy in order not to overwrite local changes."
     else
         before_update "Fixing up permissions before copying application source code."
         find /var/www/yoda-copy -type f -perm 0444 -exec chmod 0666 {} \;
         find /var/www/extuser-copy -type f -perm 0444 -exec chmod 0666 {} \;
         progress_update "Permission fixes done."
         before_update "Copying application source code to volume."
         cp -Ru /var/www/yoda-copy/. /var/www/yoda
         cp -Ru /var/www/extuser-copy/. /var/www/extuser
         progress_update "Copying application source code finished."
     fi
else progress_update "Notice: no bind mount detected. Keeping current application UID ${CURRENT_UID}"
fi

# Download EUS database dump
before_update "Downloading EUS database dump"
wget -q "https://yoda.uu.nl/yoda-docker/${DATA_VERSION}.extuser.sql.gz" -O "/download/${DATA_VERSION}.extuser.sql.gz"
progress_update "EUS database dump downloaded"

# Wait for database container to become available
before_update "Waiting for PostgreSQL container to come up ..."
export PGPASSWORD=yodadev
while ! psql -U extuser -d extuser -h extuserdb.yoda -p 5432 -c 'SELECT 1' >& /dev/null ; do
  printf "."
  sleep 0.5
done
progress_update "PostgreSQL is now up."

# Load EUS database dump
before_update "Loading EUS database data"
export PGPASSWORD=yodadev
gunzip -c "/download/${DATA_VERSION}.extuser.sql.gz" | psql -U extuser -d extuser -h extuserdb.yoda -p 5432
progress_update "EUS database data loaded"

# Configure EUS
before_update "Configuring the EUS"
cd /var/www/yoda
YODA_COMMIT=$(git rev-parse HEAD)
cd /var/www/extuser/yoda-external-user-service
EXTUSER_COMMIT=$(git rev-parse HEAD)
SECRET_KEY=$(openssl rand -base64 32)
cat << FLASKCFG > /var/www/extuser/flask.cfg
SECRET_KEY          = '$SECRET_KEY'
YODA_VERSION        = 'development'
YODA_EUS_COMMIT     = '${EXTUSER_COMMIT}-${YODA_COMMIT}'
YODA_EUS_FQDN       = 'eus.yoda'
CSRF_TOKENS_ENABLED = 'true'
API_SECRET          = 'PLACEHOLDER'
EUS_TITLE_TEXT      = 'Yoda External User Service'

# Theming configuration
YODA_THEME_PATH     = '/var/www/yoda/themes' # Path to location of themes
YODA_THEME          = 'uu'      # Reference to actual theme directory in YODA_THEME_PATH

# Email configuration
SMTP_SERVER                = 'smtp://mailpit.yoda:1025'
SMTP_USERNAME              = 'PLACEHOLDER'
SMTP_PASSWORD              = 'PLACEHOLDER'
SMTP_AUTH                  = 'false'
SMTP_STARTTLS              = 'false'
SMTP_FROM_NAME             = 'Yoda External User Service'
SMTP_FROM_EMAIL            = 'yoda@yoda.test'
SMTP_REPLYTO_NAME          = 'PLACEHOLDER'
SMTP_REPLYTO_EMAIL         = 'yoda@yoda.test'
MAIL_ENABLED               = 'true'
MAIL_TEMPLATE              = 'uu'
MAIL_TEMPLATE_DIR          = '/var/www/extuser/yoda-external-user-service/yoda_eus/templates/mail'
MAIL_ONLY_TO_VALID_ADDRESS = 'false'

# Database configuration
DB_DIALECT          = 'postgresql+psycopg2'
DB_HOST             = 'extuserdb.yoda'
DB_PORT             = '5432'
DB_NAME             = 'extuser'
DB_USER             = 'extuser'
DB_PASSWORD         = 'yodadev'
FLASKCFG

cat << YODA_EUS_NOAPI > /var/www/extuser/yoda_eus_noapi.wsgi
#!/usr/bin/env python3

import os
import sys

activate_this = '/var/www/extuser/yoda-external-user-service/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from yoda_eus import app

application = app.create_app(config_filename="/var/www/extuser/flask.cfg", enable_api=False)
YODA_EUS_NOAPI

cat << YODA_EUS_API > /var/www/extuser/yoda_eus_api.wsgi
#!/usr/bin/env python3

import os
import sys

activate_this = '/var/www/extuser/yoda-external-user-service/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from yoda_eus import app

application = app.create_app(config_filename="/var/www/extuser/flask.cfg", enable_api=True)
YODA_EUS_API

progress_update "Portal configured"

# Start Apache
touch /container_initialized
before_update "Initialization complete. Starting Apache"
start_service
