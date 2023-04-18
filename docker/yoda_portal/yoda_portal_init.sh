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
mkdir /download
cd /download
tar xvfz "${DATA_VERSION}.certbundle.tar.gz"
install -m 0644 -o irods -g irods docker.pem /etc/pki/tls/certs/localhost_and_chain.crt
install -m 0644 -o irods -g irods docker.key /etc/pki/tls/private/localhost.key
install -m 0644 -o irods -g irods dhparam.pem /etc/pki/tls/private/dhparams.pem
progress_update "Certificate data extracted"

# Configure the portal
before_update "Configuring the portal"
cd /var/www/yoda
YODA_COMMIT=$(git rev-parse HEAD)
SECRET_KEY=$(openssl rand -base64 32)
cat << FLASKCFG > /var/www/yoda/flask.cfg
import ssl
from flask import current_app as app

# General Flask configuration
SECRET_KEY          = '$SECRET_KEY'
PORTAL_TITLE_TEXT   = 'Yoda - Dev (Docker)'
YODA_VERSION        = 'development'
YODA_COMMIT         = '$YODA_COMMIT'
RESEARCH_ENABLED    = True
OPEN_SEARCH_ENABLED = True
DEPOSIT_ENABLED     = True
INTAKE_ENABLED      = True
INTAKE_EXT_TIMEOUT  = 1800
DATAREQUEST_ENABLED = True
TOKENS_ENABLED      = True
TOKEN_LIFETIME      = 72
JSON_SORT_KEYS      = False  # Check if this is still needed with Python v3.7?

# Flask-Session configuration
SESSION_TYPE                = 'filesystem'
SESSION_COOKIE_NAME         = '__Host-session'
SESSION_COOKIE_HTTPONLY     = True
SESSION_COOKIE_SECURE       = True
SESSION_COOKIE_SAMESITE     = 'Strict'
PERMANENT_SESSION_LIFETIME  = 30 * 60
SESSION_USE_SIGNER          = True
SESSION_FILE_DIR            = '/tmp/flask_session/'

# iRODS authentication configuration
IRODS_ICAT_HOSTNAME = 'provider.yoda'
IRODS_ICAT_PORT     = '1247'
IRODS_DEFAULT_ZONE  = 'tempZone'
IRODS_DEFAULT_RESC  = 'irodsResc'
IRODS_SSL_CA_FILE   = '/etc/pki/tls/certs/localhost_and_chain.crt'
IRODS_AUTH_SCHEME   = 'PAM'
IRODS_CLIENT_OPTIONS_FOR_SSL = {
    "irods_client_server_policy": "CS_NEG_REQUIRE",
    "irods_client_server_negotiation": "request_server_negotiation",
    "irods_ssl_ca_certificate_file": IRODS_SSL_CA_FILE,
    "irods_ssl_verify_server": "cert",
    "irods_encryption_key_size": 16,
    "irods_encryption_salt_size": 8,
    "irods_encryption_num_hash_rounds": 16,
    "irods_encryption_algorithm": "AES-256-CBC"
}
IRODS_SESSION_OPTIONS = {
    'ssl_context' : ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH,
        cafile=IRODS_SSL_CA_FILE,
        capath=None,
        cadata=None,
    ),
    **IRODS_CLIENT_OPTIONS_FOR_SSL,
    'authentication_scheme': IRODS_AUTH_SCHEME,
    'application_name': 'yoda-portal'
}

# OIDC configuration
OIDC_ENABLED        = True
OIDC_DOMAINS        = ['yoda.dev']
OIDC_CLIENT_ID      = 'myClientId'
OIDC_CLIENT_SECRET  = 'myClientPassword'
OIDC_CALLBACK_URI   = 'https://portal.yoda.test/user/callback'
OIDC_AUTH_BASE_URI  = 'https://oauth.mocklab.io/oauth/authorize'
OIDC_AUTH_URI       = 'https://oauth.mocklab.io/oauth/authorize?response_type=code&client_id=myClientId&redirect_uri=https://portal.yoda.test/user/callback&scope=openid&acr_values='
OIDC_LOGIN_HINT     = True
OIDC_TOKEN_URI      = 'https://oauth.mocklab.io/oauth/token'
OIDC_SCOPES         = 'openid'
OIDC_ACR_VALUES     = ''
OIDC_USERINFO_URI   = 'https://oauth.mocklab.io/userinfo'
OIDC_EMAIL_FIELD    = 'email'
OIDC_JWKS_URI       = 'https://oauth.mocklab.io/.well-known/jwks.json'
OIDC_JWT_ISSUER     = 'https://oauth.mocklab.io'
OIDC_JWT_OPTIONS    = {
    "require_exp": True,      #check that exp (expiration) claim is present
    "require_iat": False,     #check that iat (issued at) claim is present
    "require_nbf": False,     #check that nbf (not before) claim is present
    "verify_aud": True,    #check that aud (audience) claim matches audience
    "verify_iat": False,   #check that iat (issued at) claim value is an integer
    "verify_exp": True,    #check that exp (expiration) claim value is OK
    "verify_iss": True,    #check that iss (issuer) claim matches issuer
    "verify_signature": True                                #verify the JWT cryptographic signature
}

# Portal theme configuration
YODA_THEME_PATH = '/var/www/yoda/themes' # Path to location of themes
YODA_THEME = 'uu'                              # Reference to actual theme directory in YODA_THEME_PATH

# External User Service configuration
YODA_EUS_FQDN = 'eus.yoda.test'

# Data request module configuration
DATAREQUEST_HELP_CONTACT_NAME  = 'PLACEHOLDER'
DATAREQUEST_HELP_CONTACT_EMAIL = 'PLACEHOLDER'
FLASKCFG
progress_update "Portal configured"

# Start Apache
before_update "Starting Apache"
/usr/sbin/httpd -DFOREGROUND
