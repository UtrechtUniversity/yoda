#!/bin/bash

TIMESTAMP=`date +%s`
OFFSET=1
TIMESTAMP=$(( $TIMESTAMP - ($OFFSET * 60 * 60)))
/etc/irods/yoda-ruleset/tools/revision-clean-up.py ${TIMESTAMP} 'B'
