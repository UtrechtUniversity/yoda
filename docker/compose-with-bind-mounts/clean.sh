#!/bin/sh
../down.sh -v

set -e

for volume in $(find . -type d -name "v_*" -maxdepth 1)
do echo "Removing files on volume $volume ..."
   find "$volume" ! -name '.docker.gitkeep' -type f -exec rm -f {} +
   find "$volume" -type d -mindepth 1 -exec rm -rf {} +
done

echo "All files removed."
