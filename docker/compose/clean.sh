#!/bin/sh
./down.sh -v
for volume in v_extuser_app v_extuser_portal v_irods_logs v_portal_app v_yoda_ruleset
do echo "Removing files on volume $volume ..."
   find "$volume" ! -name '.docker.gitkeep' -type f -exec rm -f {} +
   find "$volume" -type d -mindepth 1 -exec rm -rf {} +
done

echo "All files removed."
