#!/bin/bash

set -e
set -u

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [
    ${CURRENT_BRANCH} == 'alpha'
    || ${CURRENT_BRANCH} == 's2'
    || ${CURRENT_BRANCH} == 'stage'
    || ${CURRENT_BRANCH} == 'master'

]; then
    echo "Please check out your feature branch first"
    exit 1
fi

# Merge the current branch to alpha
git co alpha
git merge --no-ff --no-edit $CURRENT_BRANCH
git branch -d $CURRENT_BRANCH
