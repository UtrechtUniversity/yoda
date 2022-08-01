#!/bin/bash
# Script for irods i-commands auto-completion with bash
# This script is GPL, blah blah blah...
# Bruno Bzeznik <Bruno.Bzeznik@imag.fr> 10/2011
#
# Simply source this script as follows:
#     . irods_completion.bash
# and enjoy <tab> key
# Feel free to improve!
#

# Irods command to auto-complete
command_list="ibun icd ichksum ichmod icp iget ils imeta imkdir imv iphybun iphymv irm irmtrash irsync itrim iput"

# Completion function that gets the files list from irods
_ils() {
  local cur prev dirname basename base list ilspath
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  # Set irods current directory (weird!!)
  #export irodsCwd=$(ipwd)

  # Generate the list of irods files
  if [[ $cur == "" ]] ; then
    dirname=""
    basename=""
  elif [[ $cur == */ ]] ; then
    dirname=$cur
    basename=""
  else
    dirname="$(dirname ${cur})/"
    if [[ $dirname == "." ]] ; then dirname="" ; fi
    basename=$(basename ${cur})
  fi

  # Turn relative paths into absolute paths, because ils does not respect the
  # current working directory.
  if [[ $cur == /* ]] ; then
    ilspath="${dirname}"
  else
      ilspath="$(ipwd)/${dirname}"
  fi
  list=`ils "$ilspath" | sed '/^[^ ]/d; s/^\s*//; s@^C.*/\(.*\)@\1/@' 2>/dev/null`

  # Count the number of arguments that are not options
  # (that do not begin by a dash)
  # TODO
  # to be used in place of $COMP_CWORD into the following tests

  # Case of "iput", first arg is a local file
  if [ $1 = "iput" -a $COMP_CWORD -eq 1 ]; then
    COMPREPLY=( $(compgen -o default ${cur}) )

  # Case of "iget", second arg is a local file
  elif [ $1 = "iget" -a $COMP_CWORD -eq 2 ]; then
    COMPREPLY=( $(compgen -o default ${cur}) )

  # Case of "irsync", manage i: prefix
  elif [ $1 = "irsync" ]; then
    if [[ $cur == i:* ]]; then
      base=${cur:2}
      COMPREPLY=( $(compgen -W "$list \ " ${base} ) )
    else
      COMPREPLY=( $(compgen -P i: -W "$list \ " ${cur} ) )
      COMPREPLY+=( $(compgen -o default ${cur}) )
    fi

  # General case
  else
    COMPREPLY=( $(compgen -P "$dirname" -W "$list" ${basename}) )
  fi
}

_complete_user() {
  local cur prev tmp
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  tmp=`iquest --no-page "%s" "SELECT USER_NAME where USER_TYPE != 'rodsgroup'"`

  COMPREPLY=( $(compgen -W "$tmp" "$cur") )
}

_complete_group() {
  local cur prev tmp
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  tmp=`iquest --no-page "%s" "SELECT USER_NAME where USER_TYPE = 'rodsgroup'"`

  COMPREPLY=( $(compgen -W "$tmp" "$cur") )
}

_complete_resource() {
  local cur prev tmp
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  tmp=`iquest --no-page "%s" "SELECT RESC_NAME"`

  COMPREPLY=( $(compgen -W "$tmp" "$cur") )
}

_complete_zone() {
  local cur prev tmp
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  tmp=`iquest --no-page '%s' 'SELECT ZONE_NAME'`

  COMPREPLY=( $(compgen -W "$tmp" "$cur") )
}

_complete_user_type() {
  local cur prev
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  COMPREPLY=( $(compgen -W "rodsuser rodsgroup rodsadmin" "$cur") )
}

_complete_user_prop() {
  local cur prev
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  COMPREPLY=( $(compgen -W "type zone comment info password" "$cur") )
}

_iadmin() {
  local cur prev cmds cmd
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  cmd="${COMP_WORDS[1]}"

  cmds="lu lua luan lt lr ls lz lg lgd lf mkuser moduser aua rua rpp rmuser rmdir mkresc modresc modrescdatapaths rmresc addchildtoresc rmchildfromresc mkzone modzone modzonecollacl rmzone mkgroup rmgroup atg rfg at rt spass dspass ctime suq sgq lq cu rum asq rsq help"

  if   [[ $COMP_CWORD == 1 ]]; then COMPREPLY=( $(compgen -W "$cmds" "$cur") )
  else
      if [[ $cmd =~ ^lz|modzone|rmzone$ && $COMP_CWORD == 2 ]]; then _complete_zone
    elif [[ $cmd =~ ^lu|lua|luan|moduser|aua|rua|rpp|rmuser|suq$ && $COMP_CWORD == 2 ]]; then _complete_user
    elif [[ $cmd =~ ^lg|atg|rfg|sgq$ && $COMP_CWORD == 2 ]]; then _complete_group
    elif [[ $cmd =~ ^moduser$        && $COMP_CWORD == 3 ]]; then _complete_user_prop
    elif [[ $cmd =~ ^atg|rfg$        && $COMP_CWORD == 3 ]]; then _complete_user
    elif [[ $cmd =~ ^lr|modresc|rmresc|addchildtoresc|rmchildfromresc$ && $COMP_CWORD == 2 ]]; then _complete_resource
    elif [[ $cmd =~ ^suq|sgq|addchildtoresc|rmchildfromresc$ && $COMP_CWORD == 3 ]]; then _complete_resource
    #elif [[ $cmd =~ ^moduser$        && $COMP_CWORD == 4 ]]; then
    #  if [[ $prev == "zone" ]]; then
    #  fi
    fi
  fi
}

complete -o nospace -F _iadmin iadmin

# Complete the specified commands
complete -o nospace -F _ils $command_list
