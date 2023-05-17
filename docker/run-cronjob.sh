#!/usr/bin/env bash
#
# This scripts manually triggers a job that would normally run as a cronjob in the development environment.
# Job output is shown, even if it would be discarded in a normal environment

set -e
set -x

case "$1" in

  copytovault)
    docker exec -it provider.yoda sudo -iu irods /bin/irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/retry-copy-to-vault.r
    ;;

  dailyreport)
    docker exec -it provider.yoda sudo -iu irods /bin/bash /etc/irods/yoda-ruleset/tools/mail/mail-daily-report.sh
    ;;

  dapexpiry)
    docker exec -it provider.yoda sudo -iu irods /bin/bash /etc/irods/yoda-ruleset/tools/notification/notification-data-access-token-expiry.sh
    ;;

  intakevault)
    docker exec -it provider.yoda sudo -iu irods /var/lib/irods/.irods/run-intake-movetovault.sh
    ;;

  revision)
    docker exec -it provider.yoda sudo -iu irods /bin/python /etc/irods/yoda-ruleset/tools/async-data-revision.py -v
    ;;

  revisioncleanup)
    docker exec -it provider.yoda sudo -iu irods /bin/bash /var/lib/irods/.irods/cronjob-revision-cleanup.sh
    ;;

  rum)
    docker exec -it provider.yoda sudo -iu irods /usr/bin/iadmin rum
    ;;

  statistics)
    docker exec -it provider.yoda sudo -iu irods /bin/irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/storage-statistics.r
    ;;

  weeklyreport)
    docker exec -it provider.yoda sudo -iu irods /bin/bash /etc/irods/yoda-ruleset/tools/mail/mail-weekly-report.sh
    ;;

  *)
    echo "No cronjob or invalid cronjob provided."
    ;;
esac
