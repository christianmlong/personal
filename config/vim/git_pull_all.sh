#!/bin/bash

set -u
set -e

# get the directory the script is stored in.
SCRIPTPATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PACKPATH="$SCRIPTPATH/../pack"

find "$SCRIPTPATH" -maxdepth 1 -mindepth 1 -type d -exec git --git-dir={}/.git --work-tree={} pull --ff-only \;

find "$PACKPATH" -maxdepth 5 -mindepth 1 -type d -name '.git' -exec git --git-dir={}/../.git --work-tree={}/.. pull --ff-only \;


