#!/bin/bash

TIMESTAMP=`date +%s`
OFFSET=1
TIMESTAMP=$(( $TIMESTAMP - ($OFFSET * 60 * 60)))
/usr/bin/irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/revision-clean-up.r "*endOfCalendarDay=${TIMESTAMP}" '*bucketcase="B"'
