#!/bin/sh
../down.sh -v

set -e

find . -type d -name "v_*" -maxdepth 1 | while IFS= read -r volume; do
    echo "Removing files on volume $volume ..."
    find "$volume" ! -name '.docker.gitkeep' -type f -exec rm -f {} +
    find "$volume" -type d -mindepth 1 -exec rm -rf {} +
done

echo "All files removed."
