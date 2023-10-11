#!/usr/bin/env bash
#
# This scripts manually triggers a job that would normally run as a cronjob in the development environment.
# Job output is shown, even if it would be discarded in a normal environment

set -e
set -x

if [[ -t 1 ]]
then EXEC_OPTIONS="-it"
else EXEC_OPTIONS="-i"
fi

case "$1" in

  copytovault)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/retry-copy-to-vault.r
    ;;

  dailyreport)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/bash /etc/irods/yoda-ruleset/tools/mail/mail-daily-report.sh
    ;;

  dapexpiry)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/bash /etc/irods/yoda-ruleset/tools/notification/notification-data-access-token-expiry.sh
    ;;

  intakevault)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /var/lib/irods/.irods/run-intake-movetovault.sh
    ;;

  publication)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/process-publication.r
    ;;

  revision)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/python /etc/irods/yoda-ruleset/tools/async-data-revision.py -v
    ;;

  revisioncleanup)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/bash /var/lib/irods/.irods/cronjob-revision-cleanup.sh
    ;;

  rum)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /usr/bin/iadmin rum
    ;;

  statistics)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/storage-statistics.r
    ;;

  weeklyreport)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /bin/bash /etc/irods/yoda-ruleset/tools/mail/mail-weekly-report.sh
    ;;

  moaiupdate)
    docker exec "$EXEC_OPTIONS" public.yoda sudo -iu yodadeployment /var/www/moai/yoda-moai/venv/bin/update_moai --config /var/www/moai/settings.ini yoda_moai
    ;;

  arbupdate)
    docker exec "$EXEC_OPTIONS" provider.yoda sudo -iu irods /usr/local/bin/python3 /etc/irods/yoda-ruleset/tools/arb-update-resources.py -v
    ;;

  *)
    echo "No cronjob or invalid cronjob provided."
    ;;
esac
