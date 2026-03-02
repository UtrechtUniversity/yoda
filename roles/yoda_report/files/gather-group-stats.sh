#!/bin/bash
# This script gathers group stats of Research, Vault, and Revisionsusage
# based on creation time with a 4-year cutoff, then sends the collected data
# to the reporting server

set -e
set -u

# Constants (from Ansible cron job)
INSTANCE="${INSTANCE:?INSTANCE not set}"
YODA_REPORT_SERVER_PRIV_KEY_LOC="${YODA_REPORT_SERVER_PRIV_KEY_LOC:?private key not set}"
YODA_REPORT_SERVER_USER_ACCOUNT="${YODA_REPORT_SERVER_USER_ACCOUNT:?user not set}"
YODA_REPORT_SERVER_HOST="${YODA_REPORT_SERVER_HOST:?host not set}"
YODA_REPORT_SERVER_FINANCIAL_DATA_DIR="${YODA_REPORT_SERVER_FINANCIAL_DATA_DIR:?remote dir not set}"

# Generate report and transfer
/var/lib/irods/yoda-clienttools/venv/bin/yreport_oldvsnewdata -q --use-create-time -e "$INSTANCE" -y 2.0 > "/var/yoda-financial-data/stats.yaml"
scp -i "$YODA_REPORT_SERVER_PRIV_KEY_LOC" "/var/yoda-financial-data/stats.yaml" "$YODA_REPORT_SERVER_USER_ACCOUNT@$YODA_REPORT_SERVER_HOST:$YODA_REPORT_SERVER_FINANCIAL_DATA_DIR/$INSTANCE.stats.yml"
