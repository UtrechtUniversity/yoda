#!/bin/bash
for voldir in $(find . -name "v_*" -type d -maxdepth 1)
do echo "Cleaning $voldir ..."
   rm -rf "$voldir"
   mkdir "$voldir"
   touch "$voldir/.docker.gitkeep"
done
