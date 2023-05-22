#!/bin/bash

[[ "$PAM_USER" =~ .*@.* ]] && [[ ! "$PAM_USER" =~ [.@](uu\.nl|acc\.uu\.nl)$ ]]
